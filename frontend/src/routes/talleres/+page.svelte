<script lang="ts">
	import TableTalleres from './TableTalleres.svelte';

	// MOCK DATA temporal
	const talleres = [
		{
			workshop_id: 1,
			workshop_name: "Sucursal Centro",
			address: "Av. Hidalgo #234, Hermosillo, Sonora",
			opening_hours: "08:00",
			closing_hours: "18:00"
		},
		{
			workshop_id: 2,
			workshop_name: "Sucursal Norte",
			address: "Blvd. Progreso #901, Hermosillo, Sonora",
			opening_hours: "09:00",
			closing_hours: "17:00"
		},
		{
			workshop_id: 3,
			workshop_name: "Sucursal Sur",
			address: "Av. Las Torres #501, Hermosillo, Sonora",
			opening_hours: "07:30",
			closing_hours: "16:30"
		}
	];
</script>

<div class="mt-4">
	<TableTalleres {talleres} />
</div>
