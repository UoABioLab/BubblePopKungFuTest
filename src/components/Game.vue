<template>
  <div class="game-container">
    <!-- 添加错误提示 -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
      <button @click="retryGame">Retry</button>
    </div>
    <!-- 摄像头容器 -->
    <div class="camera-container" :class="{ 'hidden': !shouldShowCamera }">
      <PoseDetection 
        @pose-update="handlePoseUpdate" 
        ref="poseDetectionRef"
      />
    </div>
    <!-- 游戏区域 -->
    <div class="game-area">
      <!-- 玩家和气球 -->
      <div class="player-container">
        <Player 
          :position="playerPosition"
          :leg-state="playerLegState"
        />
      </div>
      
      <!-- 修改气球和倒计时的显示 -->
      <div v-for="balloon in balloons" :key="balloon.id" class="balloon-container">
        <Balloon 
          :initial-position="balloon.position"
          :side="balloon.side"
          :is-stationary="balloon.isStationary"
        />
        <!-- 修改倒计时的位置，将top值调大 -->
        <div v-if="balloon.isStationary && legTimers[balloon.side].isHolding" 
             class="balloon-timer"
             :style="{
               left: `${balloon.position.x}px`,
               top: `${balloon.position.y - 350}px`
             }">
          {{ legTimers[balloon.side].countdown.toFixed(1) }}s
        </div>
      </div>
    </div>
    <!-- 游戏状态显示 -->
    <div class="game-stats">
      <div class="stat-item score">
        <span class="label">SCORE:</span>
        <span class="value">{{ score }}</span>
      </div>
      <div class="stat-item lives">
        <span class="label">LIVES:</span>
        <span class="value">{{ lives }}</span>
      </div>
      <div class="stat-item balloons">
        <span class="label">BALLOONS:</span>
        <span class="value">{{ balloonCount }}/{{ maxBalloons }}</span>
      </div>
    </div>
    <!-- 添加游戏开始/结束界面 -->
    <div v-if="!isPlaying && !countdownVisible && !calibrating" class="game-overlay">
      <div class="game-menu">
        <h2>{{ gameOver ? 'Game Over!' : 'Balloon Master' }}</h2>
        <p v-if="gameOver">Final Score: {{ score }}</p>
        <!-- 游戏结束时显示两个按钮 -->
        <div v-if="gameOver" class="game-over-buttons">
          <button @click="startGame">Play Again</button>
          <button @click="backToMenu" class="back-button">Back to Menu</button>
        </div>
        <!-- 游戏未开始时显示难度选择和返回按钮 -->
        <div v-else>
          <div class="difficulty-select">
            <h3>Select Difficulty:</h3>
            <div class="difficulty-buttons">
              <button 
                v-for="(config, diff) in GAME_CONFIG.difficulties" 
                :key="diff"
                :class="{ active: selectedDifficulty === diff }"
                @click="selectedDifficulty = diff"
              >
                {{ diff.charAt(0).toUpperCase() + diff.slice(1) }}
              </button>
            </div>
          </div>
          <div class="start-buttons">
            <button class="start-button" @click="startGame">Start Game</button>
            <!-- 添加返回主页按钮 -->
            <button class="start-button" @click="backToMain">Back to Home</button>
          </div>
        </div>
      </div>
    </div>
    <!-- 修改倒计时显示 -->
    <div v-if="countdownVisible" class="countdown-overlay">
      <div class="countdown">{{ countdown }}</div>
    </div>
    <!-- 添加校准倒计时显示 -->
    <div v-if="calibrating" class="calibration-overlay">
      <div class="calibration-message">
        Please maintain a standing position {{ calibrationTimeLeft }}s
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, reactive, onMounted, onUnmounted } from 'vue'
import PoseDetection from './PoseDetection.vue'
import Balloon from './Balloon.vue'
import Player from './Player.vue'
// 游戏配置
const GAME_CONFIG = reactive({
  initialLives: 3,
  // 移除 gameTime 配置
  // 添加气球数量配置
  balloonCounts: {
    easy: 8,
    medium: 10, 
    hard: 12
  },
  // 修改固定位置配置，将气球位置调回原位
  spawnPositions: {
    left: { 
      x: window.innerWidth * 0.25,
      y: window.innerHeight * 0.6   // 改回原来的位置
    },
    right: { 
      x: window.innerWidth * 0.75,
      y: window.innerHeight * 0.6   // 改回原来的位置
    }
  },
  playerPosition: {
    x: window.innerWidth * 0.5,     // 玩家保持在中间
    y: window.innerHeight * 0.7     // 玩家置微上移
  },
  // 完善难度设置
  difficulties: {
    easy: {
      legHoldTime: 2,     // 需要保持的时间（秒）
      spawnRate: 8000,    // 改为 8000 毫秒（8秒）
      scorePerBalloon: 10,
      penaltyScore: -0,   // 失败扣分
      responseTime: 1000  // 添加响应时间配置（毫秒）
    },
    medium: {
      legHoldTime: 3,
      spawnRate: 8000,    // 改为 8000 毫秒（8秒）
      scorePerBalloon: 15,
      penaltyScore: -0,
      responseTime: 1000
    },
    hard: {
      legHoldTime: 4,
      spawnRate: 8000,    // 改为 8000 毫秒（8秒）
      scorePerBalloon: 20,
      penaltyScore: -0,
      responseTime: 1000
    }
  }
})
// 游戏状态
const score = ref(0)
const lives = ref(3)
const balloons = ref([])
const selectedDifficulty = ref('medium')
const isPlaying = ref(false)
const gameOver = ref(false)
// 添加倒计时相关状态
const countdownVisible = ref(false)
const countdown = ref(3)
// 玩家状态
const playerPosition = ref({
  x: GAME_CONFIG.playerPosition.x,
  y: GAME_CONFIG.playerPosition.y
})
const playerLegState = ref('normal')
// 腿部计时器状态
const legTimers = reactive({
  left: {
    startTime: null,
    isHolding: false,
    countdown: 0,
    balloonId: null,
    countdownInterval: null
  },
  right: {
    startTime: null,
    isHolding: false,
    countdown: 0,
    balloonId: null,
    countdownInterval: null
  }
})
// 音效系统 - 只保留必要的音效
const sounds = reactive({
  pop: new Audio('/BubblePopKungFu/Assets/pop_sound.mp3'),  // 气球爆炸音效
  miss: new Audio('/BubblePopKungFu/Assets/splash.wav')      // 失败音效
})
// 初始化音效
const initSounds = () => {
  Object.values(sounds).forEach(sound => {
    sound.load()
    sound.volume = 0.5
  })
}
// 播放音效函数
const playSound = (soundName) => {
  try {
    if (sounds[soundName]) {
      sounds[soundName].currentTime = 0
      const playPromise = sounds[soundName].play()
      if (playPromise !== undefined) {
        playPromise.catch(error => {
          console.warn(`Error playing sound ${soundName}:`, error)
        })
      }
    }
  } catch (error) {
    console.warn(`Error with sound ${soundName}:`, error)
  }
}
// 在组件挂载时初始化音效
onMounted(() => {
  initSounds()
})
// 在组件卸载时停止所有音效
onUnmounted(() => {
  Object.values(sounds).forEach(sound => {
    sound.pause()
    sound.currentTime = 0
  })
})
// 添加背景音乐
const bgMusic = new Audio('/BubblePopKungFu/Assets/kung_fu_music.mp3')
bgMusic.loop = true  // 循环播
bgMusic.volume = 0.5 // 设置音量
// 游戏循
let gameLoop = null
let spawnTimer = null
// 开始游戏
const startGame = async () => {
  try {
    const difficulty = GAME_CONFIG.difficulties[selectedDifficulty.value]
    
    // 重置游戏状态
    score.value = 0
    lives.value = GAME_CONFIG.initialLives
    balloons.value = []
    gameOver.value = false
    balloonCount.value = 0 // 重置气球计数
    
    // 重置姿势检测的基准值
    if (poseDetectionRef.value) {
      poseDetectionRef.value.resetBaseline()
    }
    
    // 开始5秒倒计时
    countdownVisible.value = true
    for(let i = 5; i > 0; i--) {
      countdown.value = i
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
    countdownVisible.value = false
    
    // 倒计时结束开始游戏
    isPlaying.value = true
    startGameLoop()
    
    // 播放背景音乐
    bgMusic.play().catch(console.error)
    
  } catch (error) {
    console.error('Game start error:', error)
    errorMessage.value = 'Game start failed, please try again'
  }
}
// 添加气球生成状态
const balloonState = reactive({
  isGenerating: false,  // 是否正在生成气球
  lastBalloonTime: 0    // 上一个气球的生成时间
})
// 开始游戏循环
const startGameLoop = () => {
  const difficulty = GAME_CONFIG.difficulties[selectedDifficulty.value]
  
  // 清理之前的计时器
  clearInterval(gameLoop)
  clearInterval(spawnTimer)

  // 气球生成定时器
  spawnTimer = setInterval(() => {
    if (lives.value > 0) {
      createBalloon()
    }
  }, difficulty.spawnRate)

  // 游戏循环
  gameLoop = setInterval(() => {
    balloons.value = balloons.value.filter(balloon => {
      // 只处理已经在下落的气球
      if (!balloon.isStationary) {
        balloon.position.y += 5
        return balloon.position.y <= window.innerHeight - 50
      }
      return true  // 保留静止的气球，让生命周期计时器来处理它们
    })
  }, 16)
}
// 结束游戏
const endGame = () => {
  isPlaying.value = false
  gameOver.value = true
  
  // 清理计时器
  clearInterval(gameLoop)
  clearInterval(spawnTimer)
  
  // 清理所有气球
  balloons.value = []
  
  // 停止所有计时器
  Object.values(legTimers).forEach(timer => {
    if (timer.countdownInterval) {
      clearInterval(timer.countdownInterval)
    }
  })
  
  // 修改游戏结束事件数据
  emit('gameOver', {
    score: score.value,
    difficulty: selectedDifficulty.value,
    reason: lives.value <= 0 ? 'lives' : 'complete'  // 修改结束原因
  })
  
  // 停止背景音乐
  bgMusic.pause()
  bgMusic.currentTime = 0
}
// 组件卸载时清理资源
onUnmounted(() => {
  clearInterval(gameLoop)
  clearInterval(spawnTimer)
  bgMusic.pause()
  bgMusic.currentTime = 0
})
// 计算属性：是否显示摄像头
const shouldShowCamera = computed(() => {
  return countdownVisible.value || isPlaying.value
})
// 定义组件事件
const emit = defineEmits(['gameOver'])
// 生成气球
const createBalloon = () => {
  // 检查是否达到最大气球数
  if (balloonCount.value >= maxBalloons.value) {
    return
  }

  const id = Date.now()
  const side = Math.random() < 0.5 ? 'left' : 'right'
  const position = { 
    x: GAME_CONFIG.spawnPositions[side].x,
    y: GAME_CONFIG.spawnPositions[side].y
  }
  
  const balloon = {
    id,
    position,
    side,
    isStationary: true,
    showTimer: false,
    timerValue: 0,
    createdAt: Date.now(),
    lifetimeTimer: null,
    isPaused: false
  }

  balloon.lifetimeTimer = setTimeout(() => {
    handleBalloonTimeout(balloon.id)
  }, 7000)

  balloons.value.push(balloon)
  balloonCount.value++ // 增加气球计数
}

// 添加气球超时处理函数
const handleBalloonTimeout = (balloonId) => {
  const balloon = balloons.value.find(b => b.id === balloonId)
  if (balloon && balloon.isStationary && !balloon.isPaused) {
    balloon.isStationary = false
    lives.value--
    playSound('miss')
    
    if (lives.value <= 0) {
      endGame()
    }
  }
}

// 添加游戏状态检查
const checkGameState = () => {
  if (!isPlaying.value) return false
  if (!poseDetectionRef.value?.isCameraReady) {
    console.error('Camera not ready')
    endGame()
    return false
  }
  return true
}
// 修改 handlePoseUpdate 函数
const handlePoseUpdate = (pose) => {
  if (!isPlaying.value || !pose.poseLandmarks) return

  // 获取左右膝盖的关键点
  const leftKnee = pose.poseLandmarks[26]    
  const rightKnee = pose.poseLandmarks[25]   
  const leftAnkle = pose.poseLandmarks[28]   
  const rightAnkle = pose.poseLandmarks[27]  

  // 计算膝盖之间的水平距离
  const kneeDistance = leftKnee.y - rightKnee.y

  // 设置阈值
  const KNEE_THRESHOLD = 0.05

  // 判断腿部状态
  let leftLegUp = false
  let rightLegUp = false

  if (Math.abs(kneeDistance) <= KNEE_THRESHOLD) {
    // 双脚并拢站立
    leftLegUp = false
    rightLegUp = false
  } else if (kneeDistance < -KNEE_THRESHOLD) {
    // 左腿抬起 (左膝向右移动)
    leftLegUp = true
    rightLegUp = false
  } else if (kneeDistance > KNEE_THRESHOLD) {
    // 右腿抬起 (右膝向左移动)
    rightLegUp = true
    leftLegUp = false
  }

  // 添加调试日志
  if (leftLegUp || rightLegUp) {
    console.log('Knee distance:', kneeDistance.toFixed(3))
  }

  // 处理左右腿的状态
  handleLegState('left', leftLegUp)
  handleLegState('right', rightLegUp)
  
  // 更新玩家状态
  updatePlayerState(leftLegUp, rightLegUp)
}
// 修改 handleLegState 函数
const handleLegState = (side, isUp) => {
  const timer = legTimers[side]
  const difficulty = GAME_CONFIG.difficulties[selectedDifficulty.value]
  
  // 找到对应的气球
  const balloon = balloons.value.find(b => b.side === side && b.isStationary)
  
  if (balloon) {
    if (isUp && !timer.isHolding) {
      // 开始计时时暂停气球的生命周期计时器
      balloon.isPaused = true
      clearTimeout(balloon.lifetimeTimer)
      
      // 开始姿势保持计时
      timer.startTime = Date.now()
      timer.isHolding = true
      timer.countdown = difficulty.legHoldTime
      timer.balloonId = balloon.id
      
      // 显示倒计时
      balloon.showTimer = true
      balloon.timerValue = difficulty.legHoldTime

      // 开始倒计时更新
      timer.countdownInterval = setInterval(() => {
        if (timer.isHolding) {
          const timeLeft = Math.max(0, difficulty.legHoldTime - 
            (Date.now() - timer.startTime) / 1000)
          timer.countdown = timeLeft
          
          if (timeLeft === 0) {
            // 成功消除气球后检查游戏结束条件
            balloon.showTimer = false
            score.value += difficulty.scorePerBalloon
            playSound('pop')
            balloons.value = balloons.value.filter(b => b.id !== timer.balloonId)
            
            // 清理计时器状态
            clearInterval(timer.countdownInterval)
            timer.isHolding = false
            timer.startTime = null
            timer.countdown = 0
            timer.balloonId = null
            
            // 检查游戏是否结束
            checkGameEnd()
          } else {
            balloon.timerValue = timeLeft
          }
        }
      }, 100)
      
    } else if (!isUp && timer.isHolding) {
      // 放下腿时检查是否达到要求的保持时间
      const holdTime = (Date.now() - timer.startTime) / 1000
      
      if (holdTime < difficulty.legHoldTime) {
        // 没有保持足够时间就放下腿
        balloon.isStationary = false
        balloon.showTimer = false
        lives.value--
        score.value += difficulty.penaltyScore
        playSound('miss')
        
        if (lives.value <= 0) {
          endGame()
        }
      }
      
      // 清理计时器状态
      clearInterval(timer.countdownInterval)
      timer.isHolding = false
      timer.startTime = null
      timer.countdown = 0
      timer.balloonId = null
      
      // 如气球还存在且未完成,恢复生命周期计时器
      if (balloon && balloon.isStationary) {
        balloon.isPaused = false
        balloon.lifetimeTimer = setTimeout(() => {
          handleBalloonTimeout(balloon.id)
        }, 7000)
      }
    }
  }
}
// 修改 updatePlayerState 函数
const updatePlayerState = (leftLegUp, rightLegUp) => {
  // 因为在检测中已交了左右腿，所以这里也要相应交换
  if (rightLegUp && !leftLegUp) {  // 交换左右腿的判断
    playerLegState.value = 'leftUp'
  } else if (leftLegUp && !rightLegUp) {  // 交换左右腿的判断
    playerLegState.value = 'rightUp'
  } else {
    playerLegState.value = 'normal'
  }
}
// 添加连击系统
const combo = reactive({
  count: 0,
  timer: null,
  resetDelay: 2000  // 2内没有新的成功则重置连击
})
// 修改计分函数
const addScore = (baseScore) => {
  const difficulty = GAME_CONFIG.difficulties[selectedDifficulty.value]
  const comboMultiplier = Math.pow(difficulty.comboMultiplier, combo.count)
  const finalScore = Math.round(baseScore * comboMultiplier)
  score.value += finalScore
  // 更新连击
  combo.count++
  // 重置连击计时器
  clearTimeout(combo.timer)
  combo.timer = setTimeout(() => {
    combo.count = 0
  }, combo.resetDelay)
  return finalScore
}
// 修改失败处理函数
const handleFailure = () => {
  const difficulty = GAME_CONFIG.difficulties[selectedDifficulty.value]
  score.value += difficulty.penaltyScore
  lives.value--
  combo.count = 0  // 重置连击
  playSound('miss')
  if (lives.value <= 0) {
    endGame()
  }
}
// 添加返回主菜单函数
const backToMenu = () => {
  // 重置游戏状态
  gameOver.value = false
  isPlaying.value = false
  score.value = 0
  lives.value = GAME_CONFIG.initialLives
  balloons.value = []
  
  // 停止所有音效和背景音乐
  bgMusic.pause()
  bgMusic.currentTime = 0
  Object.values(sounds).forEach(sound => {
    sound.pause()
    sound.currentTime = 0
  })
  
  // 清理所有计时器
  clearInterval(gameLoop)
  clearInterval(spawnTimer)
}
// 添加 ref 来引用 PoseDetection 组件
const poseDetectionRef = ref(null)
// 添加错误状态
const errorMessage = ref('')
// 添加重试函数
const retryGame = async () => {
  errorMessage.value = ''
  try {
    await startGame()
  } catch (error) {
    errorMessage.value = 'Game start failed, please check camera permissions'
  }
}
// 添加时间格式化函数
const formatTime = (seconds) => {
  console.log('Formatting time:', seconds)  // 添加调试日志
  if (!seconds && seconds !== 0) return '0:00'
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}
// 添加校准状态
const calibrating = ref(false)
const calibrationTimeLeft = ref(5)
let calibrationTimer = null
// 添加校准提示文本
const calibrationMessage = ref('')
// 添加气球计数状态
const balloonCount = ref(0)
const maxBalloons = computed(() => GAME_CONFIG.balloonCounts[selectedDifficulty.value])
// 修改结束游戏条件
const checkGameEnd = () => {
  // 当所有气球都被处理完且没有剩余气球时，游戏结束
  if (balloonCount.value >= maxBalloons.value && balloons.value.length === 0) {
    endGame()
  }
}

// 添加返回主页函数
const backToMain = () => {
  window.location.href = 'https://uoabiolab.github.io/GameIndex/'
}
</script>
<style scoped>
.game-container {
  width: 100vw;
  height: 100vh;
  position: relative;
  overflow: hidden;
}
.game-stats {
  position: fixed;
  top: 20px;
  left: 20px;
  display: flex;
  gap: 30px;
  z-index: 9999;
  font-family: 'Arial', sans-serif;
  pointer-events: none;
}
.stat-item {
  background-color: rgba(0, 0, 0, 0.9);
  padding: 12px 24px;
  border-radius: 8px;
  color: white;
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 120px;
  justify-content: space-between;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
.stat-item.score {
  min-width: 160px;
}
.stat-item.lives {
  min-width: 120px;
}
.stat-item.timer {
  min-width: 140px;
}
.stat-item .label {
  font-size: 20px;
  font-weight: bold;
  color: #FFD700;
  letter-spacing: 1px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}
.stat-item .value {
  font-size: 28px;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}
.timer .value {
  color: #00FFFF;
  min-width: 70px;
  text-align: right;
}
.score .value {
  color: #4CAF50;
}
.lives .value {
  color: #FF4444;
}
.game-area {
  width: 100%;
  height: 100%;
  position: relative;
}
.game-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1500;
}
.game-menu {
  background-color: #fff;
  padding: 40px;
  border-radius: 10px;
  text-align: center;
}
.game-menu h2 {
  margin: 0 0 20px 0;
  color: #333;
}
.game-menu button {
  padding: 10px 20px;
  font-size: 18px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.game-menu button:hover {
  background-color: #45a049;
}
.difficulty-select {
  margin: 20px 0;
}
.difficulty-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 10px;
}
.difficulty-buttons button {
  padding: 8px 16px;
  font-size: 16px;
  background-color: #666;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}
.difficulty-buttons button.active {
  background-color: #4CAF50;
  transform: scale(1.1);
}
.difficulty-buttons button:hover {
  opacity: 0.9;
}
.start-button {
  margin-top: 20px;
}
.countdown-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.countdown-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}
.countdown {
  font-size: 120px;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}
.calibration-message {
  font-size: 24px;
  color: white;
  text-align: center;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 10px 20px;
  border-radius: 10px;
}
.camera-container {
  position: fixed;
  left: 20px;
  bottom: 20px;
  transition: opacity 0.3s ease;
  z-index: 1000;
}
.camera-container.hidden {
  opacity: 0;
  pointer-events: none;
}
/* 添加摄像头初始化关样式 */
.camera-init-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}
.camera-init-box {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
}
.error-message {
  color: red;
  margin-top: 20px;
}
.error-message button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.leg-timers {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
.timer {
  position: absolute;
  bottom: 150px;
  padding: 10px;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  border-radius: 5px;
  font-size: 24px;
}
.timer.left {
  left: 30%;
  transform: translateX(-50%);
}
.timer.right {
  right: 30%;
  transform: translateX(50%);
}
/* 添加新的动画效果 */
.balloon-pop {
  animation: pop 0.3s ease-out;
}
@keyframes pop {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(0); opacity: 0; }
}
.game-over-text {
  animation: fadeIn 0.5s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}
.game-over-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}
.game-over-content {
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  text-align: center;
}
.game-over-content button {
  margin: 10px;
  padding: 10px 20px;
  font-size: 18px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.game-over-content button:hover {
  background-color: #45a049;
}
/* 添加游戏结束按钮样式 */
.game-over-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 30px;
}
.game-over-buttons button {
  padding: 12px 24px;
  font-size: 18px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}
.game-over-buttons .back-button {
  background-color: #666;  /* 不同的颜色区分两个按钮 */
}
.game-over-buttons .back-button:hover {
  background-color: #555;
}
.game-over-buttons button:hover {
  transform: scale(1.05);
}
.error-message {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(255, 0, 0, 0.8);
  color: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  z-index: 1000;
}
.error-message button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.player-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.hold-timer {
position: absolute;
top: -450px; /* 调整位置更靠上 (原来是-360px) */
left: 50%;
transform: translateX(-50%);
background-color: rgba(255, 0, 0, 0.8);
color: #00FFFF;
padding: 60px 90px; /* 增加内边距到原来的3倍 (原来是20px 30px) */
border-radius: 50%;
font-size: 144px; /* 字体大小增加到3倍 (原来是48px) */
font-weight: bold;
min-width: 360px; /* 最小宽度增加到3倍 (原来是120px) */
min-height: 360px; /* 最小高度增加到3倍 (原来是120px) */
display: flex;
align-items: center;
justify-content: center;
box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* 阴影也相应增大 */
z-index: 100;
}
.calibration-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.calibration-message {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20px 40px;
  border-radius: 10px;
  font-size: 24px;
  color: #333;
}

.balloon-container {
  position: relative;
}

/* .balloon-timer {
  position: absolute;
  transform: translateX(-50%);
  background-color: rgba(255, 0, 0, 0.8);
  color: white;
  padding: 15px 25px;
  border-radius: 50%;
  font-size: 36px;
  font-weight: bold;
  text-align: center;
  z-index: 100;
  top: -350px;
  min-width: 60px;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
} */

.balloon-timer {
  position: absolute;
  transform: translateX(-50%);
  background-color: rgba(255, 0, 0, 0.8);
  color: white;
  padding: 30px 50px;
  border-radius: 50%;
  font-size: 72px;
  font-weight: bold;
  text-align: center;
  z-index: 100;
  top: -350px;
  min-width: 120px;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.start-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.start-button {
  padding: 10px 30px;
  min-width: 150px;
  font-size: 18px;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #4CAF50;
}

.start-button:hover {
  transform: scale(1.05);
  opacity: 0.9;
}
</style> 