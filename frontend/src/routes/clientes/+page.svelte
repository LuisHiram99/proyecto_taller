<script lang="ts">
	import TableClientes from './TableClientes.svelte';

	// Datos MOCK temporales (se reemplazarán al integrar FastAPI)
	const clientes = [
		{
			customer_id: 1,
			first_name: "Juan",
			last_name: "Pérez",
			phone: "6621234567",
			email: "juan@example.com",
			created_at: "2024-02-10 12:00:00"
		},
		{
			customer_id: 2,
			first_name: "María",
			last_name: "López",
			phone: "6629876543",
			email: "maria@example.com",
			created_at: "2024-01-15 09:30:00"
		},
		{
			customer_id: 3,
			first_name: "Pedro",
			last_name: "Ramírez",
			phone: "6628881212",
			email: "pedro@example.com",
			created_at: "2024-01-01 08:10:00"
		}
	];
</script>

<div class="mt-4">
	<TableClientes {clientes} />
</div>
