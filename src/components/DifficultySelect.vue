<template>

  <div class="difficulty-container">

    <h2>选择难度</h2>

    

    <div class="input-section">

      <label for="userId">用户ID:</label>

      <input 

        type="text" 

        id="userId" 

        v-model="userId"

        placeholder="请输入用户ID"

      >

    </div>



    <div class="difficulty-options">

      <button 

        v-for="diff in difficulties" 

        :key="diff.name"

        :class="{ active: selectedDifficulty === diff.name }"

        @click="selectDifficulty(diff)"

      >

        <h3>{{ diff.label }}</h3>

        <div class="diff-details">

          <p>生成速度: {{ diff.config.balloonSpawnRate }}s</p>

          <p>移动速度: {{ diff.config.balloonSpeed }}</p>

          <p>得分倍率: {{ diff.config.scorePerBalloon }}</p>

        </div>

      </button>

    </div>



    <div class="action-buttons">

      <button 

        class="confirm-button" 

        @click="confirmSelection"

        :disabled="!isValid"

      >

        确认

      </button>

      <button class="back-button" @click="$emit('back')">返回</button>

      <button class="home-button" @click="backToMain">返回主页</button>

    </div>

  </div>

</template>



<script setup>

import { ref, computed } from 'vue'



const difficulties = [

  {

    name: 'easy',

    label: '简单',

    config: {

      balloonSpawnRate: 2.0,

      balloonSpeed: 2,

      scorePerBalloon: 10

    }

  },

  {

    name: 'medium',

    label: '中等',

    config: {

      balloonSpawnRate: 1.5,

      balloonSpeed: 3,

      scorePerBalloon: 15

    }

  },

  {

    name: 'hard',

    label: '困难',

    config: {

      balloonSpawnRate: 1.0,

      balloonSpeed: 4,

      scorePerBalloon: 20

    }

  }

]



const userId = ref('')

const selectedDifficulty = ref('')



const isValid = computed(() => {

  return userId.value.trim() && selectedDifficulty.value

})



const selectDifficulty = (difficulty) => {

  selectedDifficulty.value = difficulty.name

}



const confirmSelection = () => {

  if (isValid.value) {

    emit('confirm', {

      userId: userId.value,

      difficulty: selectedDifficulty.value,

      config: difficulties.find(d => d.name === selectedDifficulty.value).config

    })

  }

}



const emit = defineEmits(['confirm', 'back'])



const backToMain = () => {

  window.location.href = 'https://uoabiolab.github.io/GameIndex/'

}

</script>



<style scoped>

.difficulty-container {

  padding: 30px;

  background-color: rgba(0, 0, 0, 0.8);

  border-radius: 10px;

  color: white;

}



h2 {

  text-align: center;

  margin-bottom: 30px;

  color: #FFD700;

}



.input-section {

  margin-bottom: 30px;

}



input {

  width: 100%;

  padding: 10px;

  margin-top: 5px;

  border: none;

  border-radius: 5px;

  font-size: 16px;

}



.difficulty-options {

  display: grid;

  grid-template-columns: repeat(3, 1fr);

  gap: 20px;

  margin-bottom: 30px;

}



.difficulty-options button {

  padding: 20px;

  background-color: #333;

  border: none;

  border-radius: 5px;

  color: white;

  cursor: pointer;

  transition: all 0.3s ease;

}



.difficulty-options button.active {

  background-color: #4CAF50;

  transform: scale(1.05);

}



.diff-details {

  margin-top: 10px;

  font-size: 14px;

  text-align: left;

}



.action-buttons {

  display: flex;

  justify-content: center;

  gap: 20px;

}



.confirm-button, .back-button {

  padding: 10px 30px;

  font-size: 18px;

  border: none;

  border-radius: 5px;

  cursor: pointer;

}



.confirm-button {

  background-color: #4CAF50;

  color: white;

}



.confirm-button:disabled {

  background-color: #666;

  cursor: not-allowed;

}



.back-button {

  background-color: #666;

  color: white;

}



.home-button {

  padding: 10px 30px;

  font-size: 18px;

  background-color: #ff4444;

  color: white;

  border: none;

  border-radius: 5px;

  cursor: pointer;

}



.home-button:hover {

  background-color: #cc0000;

}

</style> 
