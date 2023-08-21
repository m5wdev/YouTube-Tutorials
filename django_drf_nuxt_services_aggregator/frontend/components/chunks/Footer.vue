<template>
    <footer id="footer" class="py-4">
        <div class="container text-center">
            &copy; {{ current_year }} Servis-centers.ru
        </div>
    </footer>
</template>

<script>
export default {
    data() {
        return {
            current_year: new Date().getFullYear(),
        }
    }
}
</script>

<style>

</style>
