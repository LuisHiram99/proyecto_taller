<script lang="ts">
  import "../app.css";
  import Sidebar from "$lib/components/Sidebar.svelte";
  import Hero from "$lib/components/Hero.svelte";

  // viene de +layout.server.ts
  export let data;
</script>

{#if data.isLoggedIn}
  <!-- APP AUTENTICADA: sidebar + hero + contenido -->
  <div class="flex h-screen bg-white text-gray-800">
    <Sidebar />

    <!-- ml debe coincidir con el width del sidebar -->
    <div class="flex-1 ml-49 flex flex-col">
      <Hero empresa="Los Chinos" />

      <main class="flex-1 p-6 overflow-y-auto bg-gray-50">
        <slot />
      </main>
    </div>
  </div>
{:else}
  <!-- NO AUTENTICADO: solo mostramos el contenido (login) sin sidebar ni hero -->
  <div class="min-h-screen bg-gray-50 flex">
    <main class="flex-1 flex items-center justify-center">
      <slot />
    </main>
  </div>
{/if}
