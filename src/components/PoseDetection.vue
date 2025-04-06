<template>
  <div class="pose-detection">
    <video ref="videoRef" autoplay playsinline></video>
    <canvas ref="canvasRef" width="320" height="240"></canvas>
    <div v-if="error" class="error">
      {{ error }}
      <button @click="retryCamera">Retry</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// 使用全局变量而不是导入
const { Pose } = window
const { Camera } = window
const { drawConnectors, drawLandmarks } = window
const { POSE_CONNECTIONS } = window

const videoRef = ref(null)
const canvasRef = ref(null)
const error = ref(null)
const isCameraReady = ref(false)
const lastLeftKneeY = ref(null)
const lastRightKneeY = ref(null)

let pose = null
let camera = null
let videoStream = null
const emit = defineEmits(['pose-update'])

// 添加防抖动状态
const lastLegStates = ref({
  left: false,
  right: false
})
const stateChangeTime = ref({
  left: 0,
  right: 0
})
const DEBOUNCE_TIME = 100  // 防抖时间（毫秒）

// 添加基准值状态
const baselinePositions = ref({
  leftKneeAnkleDiff: null,
  rightKneeAnkleDiff: null,
  sampleCount: 0,  // 添加采样计数
  isCalibrating: true  // 添加校准标志
})

// 添加预热状态
const isWarmedUp = ref(false)
const warmupFrames = ref(0)
const WARMUP_REQUIRED = 30  // 需要30帧来预热

// 添加校准状态
const calibrationState = ref({
  isCalibrating: false,
  startTime: null,
  duration: 5000,  // 5秒校准时间
  samples: [],
  completed: false
})

// 分步初始化
const initializeComponents = async () => {
  try {
    console.log('Starting initialization...')
    
    // 清理之前的资源
    await cleanup()
    
    // 1. 先初始化 MediaPipe Pose 模型
    console.log('Initializing MediaPipe Pose model...')
    await initPose()
    console.log('MediaPipe Pose model initialized')
    
    // 2. 初始化摄像头
    console.log('Initializing camera...')
    await initCamera()
    console.log('Camera initialized')
    
    // 3. 等待视频元素准备就绪
    console.log('Waiting for video to be ready...')
    await waitForVideoReady()
    console.log('Video ready')
    
    // 4. 最后初始化 MediaPipe Camera
    console.log('Initializing MediaPipe Camera...')
    await initMediaPipeCamera()
    console.log('MediaPipe Camera initialized')
    
    isCameraReady.value = true
    console.log('All components initialized successfully')
  } catch (e) {
    console.error('Initialization error:', e)
    error.value = e.message
    isCameraReady.value = false
    throw e
  }
}

// 初始化摄像头
const initCamera = async () => {
  try {
    if (videoStream) {
      videoStream.getTracks().forEach(track => track.stop())
    }
    
    videoStream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: 320,
        height: 240,
        facingMode: 'user',
        frameRate: { ideal: 30, min: 20 }
      }
    })
    
    if (!videoRef.value) {
      throw new Error('Video element not found')
    }
    
    videoRef.value.srcObject = videoStream
    videoRef.value.muted = true
  } catch (e) {
    console.error('Camera access error:', e)
    throw new Error(`Camera access failed: ${e.message}`)
  }
}

// 等待视频元素准备就绪
const waitForVideoReady = async () => {
  if (!videoRef.value) throw new Error('Video element not found')
  
  console.log('Waiting for video to be ready...')
  await new Promise((resolve) => {
    videoRef.value.onloadedmetadata = () => {
      console.log('Video metadata loaded')
      resolve()
    }
  })
  
  await videoRef.value.play()
  console.log('Video playback started')
}

// 初始化 MediaPipe Pose
const initPose = async () => {
  return new Promise((resolve, reject) => {
    try {
      pose = new Pose({
        locateFile: (file) => {
          return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`
        }
      })

      pose.setOptions({
        modelComplexity: 1,
        smoothLandmarks: true,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
      })

      pose.onResults(onResults)
      
      // 等待模型准备就绪
      pose.initialize().then(() => {
        console.log('Pose model ready')
        resolve()
      }).catch(reject)
    } catch (error) {
      reject(error)
    }
  })
}

// 初始化 MediaPipe Camera
const initMediaPipeCamera = async () => {
  if (camera) {
    await camera.stop()
    camera = null
  }

  camera = new Camera(videoRef.value, {
    onFrame: async () => {
      if (pose && videoRef.value.readyState === 4) {
        try {
          await pose.send({ image: videoRef.value })
        } catch (error) {
          console.error('Frame processing error:', error)
        }
      }
    },
    width: 320,
    height: 240
  })

  await camera.start()
}

// 处理姿势识别结果
const onResults = (results) => {
  if (!results.poseLandmarks || !canvasRef.value) return
  
  const canvasCtx = canvasRef.value.getContext('2d')
  canvasCtx.save()
  canvasCtx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height)
  
  // 绘制摄像头画面
  canvasCtx.drawImage(results.image, 0, 0, canvasRef.value.width, canvasRef.value.height)

  if (results.poseLandmarks) {
    // 添加预热和校准逻辑
    if (!isWarmedUp.value) {
      warmupFrames.value++
      if (warmupFrames.value >= WARMUP_REQUIRED) {
        console.log('Pose detection warmed up, starting calibration')
        isWarmedUp.value = true
        // 开始校准
        calibrationState.value.isCalibrating = true
        calibrationState.value.startTime = Date.now()
      }
      return
    }

    // 校准过程
    if (calibrationState.value.isCalibrating) {
      const leftKnee = results.poseLandmarks[26]
      const rightKnee = results.poseLandmarks[25]
      const leftAnkle = results.poseLandmarks[28]
      const rightAnkle = results.poseLandmarks[27]

      // 收集校准样本
      calibrationState.value.samples.push({
        leftDiff: leftKnee.y - leftAnkle.y,
        rightDiff: rightKnee.y - rightAnkle.y
      })

      // 检查校准是否完成
      const elapsedTime = Date.now() - calibrationState.value.startTime
      if (elapsedTime >= calibrationState.value.duration) {
        // 计算平均值
        const avgSamples = calibrationState.value.samples.reduce((acc, sample) => {
          acc.leftDiff += sample.leftDiff
          acc.rightDiff += sample.rightDiff
          return acc
        }, { leftDiff: 0, rightDiff: 0 })

        avgSamples.leftDiff /= calibrationState.value.samples.length
        avgSamples.rightDiff /= calibrationState.value.samples.length

        console.log('Calibration completed:', avgSamples)
        
        // 完成校准
        calibrationState.value.isCalibrating = false
        calibrationState.value.completed = true
      }
      return
    }

    // 只有在预热和校准都完成后才处理姿势数据
    if (isWarmedUp.value && calibrationState.value.completed) {
      // 创建新的姿势数据副本
      const swappedResults = {
        ...results,
        poseLandmarks: [...results.poseLandmarks]
      }

      // 交换左右腿的关键点
      // 膝盖 (左膝 25 <-> 右膝 26)
      const tempKnee = swappedResults.poseLandmarks[25]
      swappedResults.poseLandmarks[25] = swappedResults.poseLandmarks[26]
      swappedResults.poseLandmarks[26] = tempKnee
      
      // 脚踝 (左脚踝 27 <-> 右脚踝 28)
      const tempAnkle = swappedResults.poseLandmarks[27]
      swappedResults.poseLandmarks[27] = swappedResults.poseLandmarks[28]
      swappedResults.poseLandmarks[28] = tempAnkle

      // 获取点
      const leftKnee = swappedResults.poseLandmarks[25]
      const rightKnee = swappedResults.poseLandmarks[26]
      const leftAnkle = swappedResults.poseLandmarks[27]
      const rightAnkle = swappedResults.poseLandmarks[28]

      // 修改判断逻辑：膝盖的 y 坐标要大于脚踝的 y 坐标
      const THRESHOLD = -0.185
      const leftLegUp = leftKnee.y > leftAnkle.y + THRESHOLD
      const rightLegUp = rightKnee.y > rightAnkle.y + THRESHOLD

      // 设置姿势状态
      swappedResults.leftLegUp = leftLegUp
      swappedResults.rightLegUp = rightLegUp

      // 添加调试日志
      if (leftLegUp || rightLegUp) {
        console.log('Leg lift detected:', {
          left: leftLegUp ? `Height diff: ${(leftKnee.y - leftAnkle.y).toFixed(3)}` : 'down',
          right: rightLegUp ? `Height diff: ${(rightKnee.y - rightAnkle.y).toFixed(3)}` : 'down'
        })
      }

      // 只有在预热和校准都完成后才发送姿势数据
      emit('pose-update', swappedResults)

      // 绘制骨架
      drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS, {
        color: '#00FF00',
        lineWidth: 2
      })
      drawLandmarks(canvasCtx, results.poseLandmarks, {
        color: '#FF0000',
        lineWidth: 1,
        radius: 3
      })
    }
  }
  
  canvasCtx.restore()
}

// 修改 resetBaseline 函数
const resetBaseline = () => {
  calibrationState.value = {
    isCalibrating: false,
    startTime: null,
    duration: 5000,
    samples: [],
    completed: false
  }
  isWarmedUp.value = false
  warmupFrames.value = 0
  console.log('Reset calibration state')
}

// 修改 cleanup 函数，添加基准值重置
const cleanup = async () => {
  console.log('Cleaning up resources...')
  
  if (camera) {
    try {
      await camera.stop()
    } catch (e) {
      console.error('Error stopping camera:', e)
    }
    camera = null
  }
  
  if (pose) {
    try {
      await pose.close()
    } catch (e) {
      console.error('Error closing pose:', e)
    }
    pose = null
  }
  
  if (videoStream) {
    videoStream.getTracks().forEach(track => {
      try {
        track.stop()
      } catch (e) {
        console.error('Error stopping track:', e)
      }
    })
    videoStream = null
  }
  
  if (videoRef.value) {
    videoRef.value.srcObject = null
  }
  
  // 重置基准值
  resetBaseline()
  
  isCameraReady.value = false
}

// 添加重试机制
const retryCamera = async () => {
  console.log('Retrying camera initialization...')
  error.value = null
  await cleanup()
  try {
    await initializeComponents()
  } catch (e) {
    console.error('Retry failed:', e)
    error.value = '摄像头初始化失败，请刷新页面重试'
  }
}

// 组件挂载时初始化
onMounted(async () => {
  console.log('PoseDetection component mounted')
  try {
    await initializeComponents()
  } catch (e) {
    console.error('Mount initialization error:', e)
  }
})

// 组件卸载时确保清理资源
onUnmounted(() => {
  console.log('PoseDetection component unmounting')
  cleanup()
})

// 暴露必要的方法和状态
defineExpose({
  isCameraReady,
  retryCamera,
  cleanup,
  resetBaseline  // 暴露重置基准值的方法
})
</script>

<style scoped>
.pose-detection {
  position: relative;
  width: 320px;
  height: 240px;
}

video {
  position: absolute;
  width: 100%;
  height: 100%;
  transform: scaleX(-1);
}

canvas {
  position: absolute;
  width: 100%;
  height: 100%;
  transform: scaleX(-1);
}

.error {
  position: absolute;
  bottom: -40px;
  left: 0;
  width: 100%;
  padding: 8px;
  background-color: rgba(255, 0, 0, 0.8);
  color: white;
  text-align: center;
  font-size: 14px;
}

.error button {
  margin-left: 10px;
  padding: 4px 8px;
  background-color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style> 
