<template>
  <div class="test-container">
    <!-- 摄像头和姿势检测 -->
    <div class="camera-container">
      <PoseDetection @pose-update="handlePoseUpdate" />
    </div>

    <!-- 状态显示 -->
    <div class="status-display">
      <div class="leg-status">
        <div :class="['status-box', { active: leftLegUp }]">
          左腿: {{ leftLegUp ? '抬起' : '放下' }}
        </div>
        <div :class="['status-box', { active: rightLegUp }]">
          右腿: {{ rightLegUp ? '抬起' : '放下' }}
        </div>
      </div>
      <!-- 简化的调试信息 -->
      <div class="debug-info" v-if="debugInfo">
        <div>左腿差值: {{ debugInfo.leftDiff }}</div>
        <div>右腿差值: {{ debugInfo.rightDiff }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import PoseDetection from './PoseDetection.vue'

const leftLegUp = ref(false)
const rightLegUp = ref(false)
const debugInfo = ref(null)

const handlePoseUpdate = (pose) => {
  if (!pose.poseLandmarks) return

  const leftKnee = pose.poseLandmarks[26]
  const rightKnee = pose.poseLandmarks[25]
  const leftAnkle = pose.poseLandmarks[28]
  const rightAnkle = pose.poseLandmarks[27]

  // 计算差值：膝盖y坐标减去脚踝y坐标
  // 正常站立时约为-0.2，抬腿时差值会变大（接近-0.16或更大）
  const leftDiff = leftKnee.y - leftAnkle.y
  const rightDiff = rightKnee.y - rightAnkle.y

  // 简化调试信息
  debugInfo.value = {
    leftDiff: leftDiff.toFixed(3),
    rightDiff: rightDiff.toFixed(3)
  }

  // 判断抬腿状态：当差值大于-0.16时判定为抬腿
  const THRESHOLD = -0.16
  leftLegUp.value = leftDiff > THRESHOLD
  rightLegUp.value = rightDiff > THRESHOLD

  // 添加调试日志
  if (leftLegUp.value || rightLegUp.value) {
    console.log('Leg lift:', {
      left: leftDiff.toFixed(3),
      right: rightDiff.toFixed(3)
    })
  }
}
</script>

<style scoped>
.test-container {
  display: flex;
  gap: 20px;
  padding: 20px;
}

.camera-container {
  width: 320px;
  height: 240px;
}

.status-display {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.leg-status {
  display: flex;
  gap: 20px;
}

.status-box {
  padding: 20px;
  border-radius: 8px;
  background-color: #333;
  color: white;
  min-width: 120px;
  text-align: center;
}

.status-box.active {
  background-color: #4CAF50;
}

.debug-info {
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
  font-family: monospace;
  font-size: 18px;
  line-height: 1.5;
}
</style> 