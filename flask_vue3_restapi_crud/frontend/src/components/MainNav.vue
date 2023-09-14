<script setup>
import { RouterLink } from 'vue-router'
</script>


<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container">
            <RouterLink class="navbar-brand" exact-active-class="" active-class="" to="/">Flask + Vue3 REST API</RouterLink>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <RouterLink class="nav-link" exact-active-class="active" active-class="" to="/">Home</RouterLink>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>
