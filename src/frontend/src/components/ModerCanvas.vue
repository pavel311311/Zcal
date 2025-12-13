<template>
    <div>
        <svg width="350" height="150">
            <line v-for="(line, i) in lines" :key="i" :x1="line.x1" :y1="line.y1" :x2="line.x2" :y2="line.y2"
                :stroke-width="line.width" :stroke="line.color" />
        </svg>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const lines = ref([]);

// 仅加载JSON并渲染
onMounted(async () => {
    const res = await fetch('/shapes.json');
    const data = await res.json();
    lines.value = data.lines;
});


</script>