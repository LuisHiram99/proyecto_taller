<script lang="ts">
	export let clientes = [];
</script>

<div class="bg-white shadow-sm border border-gray-200 rounded-lg p-6">
	<h2 class="text-lg font-semibold text-gray-700 mb-4">
		Clientes registrados
	</h2>

	<div class="overflow-x-auto">
		<table class="w-full text-sm text-gray-700 border-collapse">
			<thead>
				<tr class="bg-gray-100 text-gray-600 uppercase text-xs">
					<th class="px-4 py-3 text-left">Id</th>
					<th class="px-4 py-3 text-left">Nombre</th>
					<th class="px-4 py-3 text-left">Teléfono</th>
					<th class="px-4 py-3 text-left">Correo</th>
					<th class="px-4 py-3 text-left">Fecha registro</th>
					<th class="px-4 py-3 text-center">Acción</th>
				</tr>
			</thead>

			<tbody>
				{#each clientes as c, i}
					<tr class={i % 2 === 0 ? "bg-white" : "bg-gray-50"}>
						<td class="px-4 py-3">{c.customer_id}</td>
						<td class="px-4 py-3">{c.first_name} {c.last_name}</td>
						<td class="px-4 py-3">{c.phone}</td>
						<td class="px-4 py-3">{c.email || "—"}</td>
						<td class="px-4 py-3">{new Date(c.created_at).toLocaleString()}</td>

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
