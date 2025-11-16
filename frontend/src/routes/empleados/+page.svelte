<script lang="ts">
	import TableEmpleados from './TableEmpleados.svelte';

	// MOCK DATA
	const empleados = [
		{
			worker_id: 1,
			first_name: "Luis",
			last_name: "Martínez",
			phone: "6621234567",
			position: "Mecánico General",
			nickname: "El Güero",
			workshop_id: 1
		},
		{
			worker_id: 2,
			first_name: "Raúl",
			last_name: "Soto",
			phone: "6629876543",
			position: "Eléctrico Automotriz",
			nickname: "Soto",
			workshop_id: 1
		},
		{
			worker_id: 3,
			first_name: "Miguel",
			last_name: "Valenzuela",
			phone: "6628883311",
			position: "Diagnóstico",
			nickname: "Mike",
			workshop_id: 2
		}
	];
</script>

<div class="mt-4">
	<TableEmpleados {empleados} />
</div>
