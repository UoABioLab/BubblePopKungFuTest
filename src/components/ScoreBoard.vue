<template>
  <div class="scoreboard-container">
    <h2>排行榜</h2>
    
    <div class="difficulty-filter">
      <button 
        v-for="diff in difficulties" 
        :key="diff"
        :class="{ active: selectedDifficulty === diff }"
        @click="selectedDifficulty = diff"
      >
        {{ difficultyLabels[diff] }}
      </button>
    </div>

    <div class="scores-list">
      <div class="score-header">
        <span>排名</span>
        <span>用户ID</span>
        <span>得分</span>
        <span>时间</span>
      </div>
      
      <div 
        v-for="(score, index) in filteredScores" 
        :key="index"
        class="score-item"
        :class="{ 'highlight': score.userId === currentUserId }"
      >
        <span>{{ index + 1 }}</span>
        <span>{{ score.userId }}</span>
        <span>{{ score.score }}</span>
        <span>{{ formatDate(score.date) }}</span>
      </div>
    </div>

    <button class="back-button" @click="$emit('back')">返回</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const difficulties = ['easy', 'medium', 'hard']
const difficultyLabels = {
  easy: '简单',
  medium: '中等',
  hard: '困难'
}

const selectedDifficulty = ref('medium')
const currentUserId = ref('')

// 模拟数据，实际应该从后端获取
const scores = ref([
  { userId: 'player1', score: 1000, difficulty: 'easy', date: new Date() },
  { userId: 'player2', score: 1500, difficulty: 'medium', date: new Date() },
  { userId: 'player3', score: 2000, difficulty: 'hard', date: new Date() },
])

const filteredScores = computed(() => {
  return scores.value
    .filter(score => score.difficulty === selectedDifficulty.value)
    .sort((a, b) => b.score - a.score)
})

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}

defineEmits(['back'])
</script>

<style scoped>
.scoreboard-container {
  padding: 30px;
  background-color: rgba(0, 0, 0, 0.8);
  border-radius: 10px;
  color: white;
}

h2 {
  text-align: center;
  color: #FFD700;
  margin-bottom: 30px;
}

.difficulty-filter {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 30px;
}

.difficulty-filter button {
  padding: 10px 20px;
  background-color: #333;
  border: none;
  border-radius: 5px;
  color: white;
  cursor: pointer;
}

.difficulty-filter button.active {
  background-color: #4CAF50;
}

.scores-list {
  margin-bottom: 30px;
}

.score-header, .score-item {
  display: grid;
  grid-template-columns: 0.5fr 2fr 1fr 1fr;
  padding: 10px;
  text-align: center;
}

.score-header {
  background-color: rgba(255, 255, 255, 0.1);
  font-weight: bold;
}

.score-item {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.score-item.highlight {
  background-color: rgba(76, 175, 80, 0.2);
}

.back-button {
  display: block;
  margin: 0 auto;
  padding: 10px 30px;
  background-color: #666;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.back-button:hover {
  background-color: #777;
}
</style> 