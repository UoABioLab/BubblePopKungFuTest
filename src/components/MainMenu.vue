<template>
  <div class="menu-container">
    <h1>气球大师</h1>
    <div class="menu-buttons">
      <button @click="$emit('start')">开始游戏</button>
      <button @click="$emit('difficulty')">难度设置</button>
      <button @click="$emit('scoreboard')">排行榜</button>
      <button @click="backToMain" class="back-button">返回主页</button>
    </div>
    <div class="instructions">
      <h3>游戏说明:</h3>
      <ul>
        <li>1. 选择难度级别</li>
        <li>2. 左脚踢左边气球</li>
        <li>3. 右脚踢右边气球</li>
        <li>4. 不要让气球碰到地面</li>
        <li>5. 开始游戏吧!</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
defineEmits(['start', 'difficulty', 'scoreboard'])

const backToMain = () => {
  console.log('Redirecting to main page...')
  window.location.href = 'https://uoabiolab.github.io/GameIndex/'
}
</script>

<style scoped>
.menu-container {
  padding: 40px;
  background-color: rgba(0, 0, 0, 0.8);
  border-radius: 10px;
  color: white;
  text-align: center;
}

h1 {
  font-size: 48px;
  margin-bottom: 40px;
  color: #FFD700;
}

.menu-buttons {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 40px;
}

button {
  padding: 15px 30px;
  font-size: 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: transform 0.2s;
}

button:hover {
  transform: scale(1.05);
  background-color: #45a049;
}

.instructions {
  text-align: left;
  margin-top: 30px;
}

.instructions h3 {
  color: #FFD700;
  margin-bottom: 15px;
}

.instructions ul {
  list-style: none;
  padding: 0;
}

.instructions li {
  margin: 10px 0;
  font-size: 16px;
}

.back-button {
  background-color: #ff4444 !important; /* 使用不同的颜色区分 */
}

.back-button:hover {
  background-color: #cc0000 !important;
}
</style> 