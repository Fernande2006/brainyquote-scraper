<template>
  <div class="p-8 max-w-lg mx-auto">
    <h1 class="text-2xl font-bold mb-4">BrainyQuote Scraper</h1>

    <input v-model="topic" placeholder="Entrez un sujet" class="border p-2 rounded w-full mb-4" />

    <div class="flex space-x-2 mb-4">
      <button @click="startScraper" :disabled="scraping" class="bg-blue-500 text-white px-4 py-2 rounded">
        Lancer le scraper
      </button>
      <button @click="stopScraper" :disabled="!scraping" class="bg-red-500 text-white px-4 py-2 rounded">
        Arrêter le scraper
      </button>
    </div>

    <div v-if="message" class="mb-4 p-2 border rounded">
      {{ message }}
    </div>

    <div class="flex space-x-2">
      <a href="http://localhost:8000/quotes/csv" class="bg-green-500 text-white px-4 py-2 rounded" download>
        Télécharger CSV
      </a>
      <a href="http://localhost:8000/quotes/json" class="bg-yellow-500 text-black px-4 py-2 rounded" target="_blank">
        Télécharger JSON
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"

const topic = ref("")
const message = ref("")
const scraping = ref(false)
let controller = null

const startScraper = async () => {
  if (!topic.value) return alert("Entrez un sujet !")

  scraping.value = true
  message.value = "Scraper en cours..."
  controller = new AbortController()

  try {
    const res = await axios.post(
      "http://localhost:8000/scrape",
      { topic: topic.value },
      { signal: controller.signal }
    )
    message.value = res.data.message
  } catch (err) {
    message.value = err.name === "CanceledError" ? "Scraper arrêté." : "Erreur lors du lancement du scraper."
  } finally {
    scraping.value = false
    controller = null
  }
}

const stopScraper = () => {
  if (controller) controller.abort()
}
</script>