<template>
  <div class="gameover-container">
    <h2>游戏结束</h2>
    
    <div class="score-display">
      <h3>最终得分</h3>
      <div class="score">{{ score }}</div>
    </div>

    <div class="stats">
      <div class="stat-item">
        <span>难度:</span>
        <span>{{ difficultyLabel }}</span>
      </div>
      <div class="stat-item">
        <span>用户ID:</span>
        <span>{{ userId }}</span>
      </div>
      <div class="stat-item">
        <span>游戏时长:</span>
        <span>{{ gameTime }}秒</span>
      </div>
    </div>

    <div class="action-buttons">
      <button @click="$emit('restart')">再玩一次</button>
      <button @click="$emit('menu')">返回主菜单</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  score: {
    type: Number,
    required: true
  },
  difficulty: {
    type: String,
    required: true
  },
  userId: {
    type: String,
    required: true
  },
  gameTime: {
    type: Number,
    required: true
  }
})

const difficultyLabel = computed(() => {
  const labels = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  }
  return labels[props.difficulty] || props.difficulty
})

defineEmits(['restart', 'menu'])
</script>

<style scoped>
.gameover-container {
  padding: 40px;
  background-color: rgba(0, 0, 0, 0.8);
  border-radius: 10px;
  color: white;
  text-align: center;
}

h2 {
  color: #FFD700;
  margin-bottom: 30px;
}

.score-display {
  margin: 30px 0;
}

.score {
  font-size: 64px;
  color: #4CAF50;
  margin: 20px 0;
}

.stats {
  margin: 30px 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

button {
  padding: 15px 30px;
  font-size: 18px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: transform 0.2s;
}

button:first-child {
  background-color: #4CAF50;
  color: white;
}

button:last-child {
  background-color: #666;
  color: white;
}

button:hover {
  transform: scale(1.05);
}
</style> 