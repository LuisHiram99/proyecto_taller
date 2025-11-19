<script lang="ts">
	// Datos MOCK de ejemplo (temporal)
	const trabajos = [
		{
			id: 2782,
			fecha: "2025-07-18 12:07:54",
			cliente: "Juan Perez",
			vehiculo: "Nissan Versa 2019",
			estado: "Finalizado"
		},
		{
			id: 1070,
			fecha: "2023-11-01 10:11:26",
			cliente: "Maria López",
			vehiculo: "Honda Civic 2018",
			estado: "En proceso"
		},
		{
			id: 993,
			fecha: "2023-10-05 10:10:09",
			cliente: "Carlos Rivera",
			vehiculo: "Chevrolet Spark 2017",
			estado: "Pendiente"
		},
		{
			id: 992,
			fecha: "2023-10-05 10:10:59",
			cliente: "Admin A",
			vehiculo: "Toyota Corolla 2020",
			estado: "Finalizado"
		},
		{
			id: 991,
			fecha: "2023-10-05 10:10:41",
			cliente: "Luis Mendoza",
			vehiculo: "Ford Fiesta 2015",
			estado: "Pendiente"
		}
	];
</script>

<!-- CONTENEDOR PRINCIPAL -->
<div class="bg-white shadow-sm border border-gray-200 rounded-lg p-6 mt-4">
	<h2 class="text-lg font-semibold text-gray-700 mb-4">
		Últimos trabajos realizados
	</h2>

	<div class="overflow-x-auto">
		<table class="w-full text-sm text-gray-700 border-collapse">
			<thead>
				<tr class="bg-gray-100 text-gray-600 uppercase text-xs">
					<th class="px-4 py-3 text-left">Id</th>
					<th class="px-4 py-3 text-left">Fecha</th>
					<th class="px-4 py-3 text-left">Cliente</th>
					<th class="px-4 py-3 text-left">Vehículo</th>
					<th class="px-4 py-3 text-left">Estado</th>
					<th class="px-4 py-3 text-center">Acción</th>
				</tr>
			</thead>

			<tbody>
				{#each trabajos as t, i}
					<tr class={i % 2 === 0 ? "bg-white" : "bg-gray-200"}>
						<td class="px-4 py-3">{t.id}</td>
						<td class="px-4 py-3">{t.fecha}</td>
						<td class="px-4 py-3">{t.cliente}</td>
						<td class="px-4 py-3">{t.vehiculo}</td>
						<td class="px-4 py-3">
							{#if t.estado === "Finalizado"}
								<span class="px-2 py-1 rounded text-xs bg-green-100 text-green-700">
									{t.estado}
								</span>
							{:else if t.estado === "En proceso"}
								<span class="px-2 py-1 rounded text-xs bg-blue-100 text-blue-700">
									{t.estado}
								</span>
							{:else}
								<span class="px-2 py-1 rounded text-xs bg-yellow-100 text-yellow-700">
									{t.estado}
								</span>
							{/if}
						</td>

						<td class="px-4 py-3 text-center">
							<button
								class="w-7 h-7 rounded bg-gray-200 hover:bg-gray-300 flex items-center justify-center transition"
								title="Ver detalles"
							>
								<svg class="w-4 h-4 text-gray-700" fill="currentColor" viewBox="0 0 20 20">
									<path
										d="M10 3c-4.5 0-8 4-8 7s3.5 7 8 7 8-4 8-7-3.5-7-8-7zm0 12c-2.8 0-5-2.5-5-5s2.2-5 5-5 5 2.5 5 5-2.2 5-5 5zm0-8c-.6 0-1 .5-1 1v2c0 .6.4 1 1 1s1-.4 1-1V8c0-.5-.4-1-1-1z"
									/>
								</svg>
							</button>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
