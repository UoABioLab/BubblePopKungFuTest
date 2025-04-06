<template>
  <div class="player" :style="playerStyle">
    <img :src="currentImage" alt="player" />
  </div>
</template>
<script setup>
import { ref, computed } from 'vue'
const props = defineProps({
  position: {
    type: Object,
    required: true
  },
  legState: {
    type: String,
    default: 'normal' // 'normal', 'leftUp', 'rightUp'
  }
})
// 根据不同的腿部状态显示不同的图片
const currentImage = computed(() => {
  switch (props.legState) {
    case 'leftUp':
      return '/BubblePopKungFu/Assets/yellow_left.png'
    case 'rightUp':
      return '/BubblePopKungFu/Assets/yellow_right.png'
    default:
      return '/BubblePopKungFu/Assets/yellow_front.png'
  }
})
// 计算玩家位置样式
const playerStyle = computed(() => ({
  left: `${props.position.x}px`,
  top: `${props.position.y}px`
}))
</script>
<style scoped>
.player {
  position: absolute;
  width: 300px;  /* 增加玩家大小 */
  height: 300px;
  transform: translate(-50%, -50%); /* 使用 transform 来居中玩家 */
}
.player img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style> 
