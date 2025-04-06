<template>
  <div 
    class="balloon" 
    :style="{ 
      left: `${position.x}px`, 
      top: `${position.y}px`
    }"
    :class="{ 
      'popping': isPopping,
      'falling': !isStationary 
    }"
  >
    <img :src="balloonImage" :alt="side + ' balloon'" />
    <div v-if="showTimer" class="timer">
      {{ timerValue.toFixed(1) }}s
    </div>
  </div>
</template>
<script setup>
import { ref, computed } from 'vue'
const props = defineProps({
  initialPosition: {
    type: Object,
    required: true
  },
  side: {
    type: String,
    required: true
  },
  isStationary: {
    type: Boolean,
    default: true
  },
  showTimer: {
    type: Boolean,
    default: false
  },
  timerValue: {
    type: Number,
    default: 0
  }
})
const position = ref(props.initialPosition)
const isPopping = ref(false)
// 根据side选择气球图片
const balloonImage = computed(() => {
  return props.side === 'left' 
    ? '/BubblePopKungFu/Assets/pink_balloon.png'
    : '/BubblePopKungFu/Assets/green_balloon.png'
})
</script>
<style scoped>
.balloon {
  position: absolute;
  width: 150px;
  height: 150px;
  transform: translate(-50%, -50%);
  z-index: 10;
}
.balloon.falling {
  transition: top 0.5s linear;
}
.balloon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.timer {
  position: absolute;
  top: -60px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 8px 15px;
  border-radius: 5px;
  font-size: 24px;
  font-weight: bold;
  z-index: 11;
}
.popping {
  animation: pop 0.3s ease-out forwards;
}
@keyframes pop {
  0% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.2); }
  100% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
}
.falling {
  animation: fall 1s linear forwards;
}
@keyframes fall {
  to {
    transform: translate(-50%, -50%) translateY(100vh);
  }
}
</style> 
