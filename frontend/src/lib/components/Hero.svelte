<script lang="ts">
  import { pageMetadata } from "$lib/state/pageMetadata";

  export let empresa = "Taller Mecánico Centro";
  export let descripcion = "Taller de elevadores y manijas";

  // Título dinámico desde metadata del store
  $: titulo = $pageMetadata.title ?? "Inicio";

  let sucursales = ["Sucursal Centro", "Sucursal Norte", "Sucursal Sur"];
  let sucursalSeleccionada = sucursales[0];

  function logout() {
    localStorage.removeItem("token");
    window.location.href = "/login";
  }

  // Breadcrumb sencillo basado en el título
  $: breadcrumbItems =
    titulo === "Inicio"
      ? [{ label: "Inicio", path: "/" }]
      : [
          { label: "Inicio", path: "/" },
          { label: titulo, path: "" },
        ];
</script>

<header class="w-full bg-white text-gray-800 border-b border-gray-200">
  <!-- fila principal: logo + info del taller / selector + salir -->
  <div class="flex items-center justify-between px-6 py-3">
    <!-- IZQUIERDA -->
    <div class="flex items-center gap-4">
      <img
        src="/img/logo/logo-chinos.jpeg"
        alt="logo"
        class="w-10 h-10 rounded-full object-cover"
      />

      <div class="flex flex-col leading-tight">
        <!-- descripción pequeña -->
        <span class="text-xs text-gray-500">{descripcion}</span>
        <!-- nombre del taller -->
        <span class="text-lg font-semibold text-gray-800">{empresa}</span>
      </div>
    </div>

    <!-- DERECHA -->
    <div class="flex items-center gap-4">
      <select
        bind:value={sucursalSeleccionada}
        class="bg-white border border-gray-300 rounded-lg pr-8 pl-4 py-2 text-sm
					   focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
      >
        {#each sucursales as s}
          <option value={s}>{s}</option>
        {/each}
      </select>

      <form method="POST" action="/logout">
        <button
          type="submit"
          class="px-4 py-1.5 rounded bg-red-600 hover:bg-red-700 text-white text-sm font-medium transition-colors"
        >
          Salir
        </button>
      </form>

      <!-- BREADCRUMB ABAJO -->
      <nav class="px-6 pb-3" aria-label="Breadcrumb">
        <ol class="flex items-center gap-1 text-sm text-gray-500">
          {#each breadcrumbItems as item, index}
            <li class="flex items-center">
              {#if index > 0}
                <span class="mx-1 text-gray-400">/</span>
              {/if}

              {#if index === breadcrumbItems.length - 1 || !item.path}
                <span class="font-medium text-gray-500">{item.label}</span>
              {:else}
                <a href={item.path} class="hover:text-teal-700 text-teal-600">
                  {item.label}
                </a>
              {/if}
            </li>
          {/each}
        </ol>
      </nav>
    </div>
  </div>
</header>
