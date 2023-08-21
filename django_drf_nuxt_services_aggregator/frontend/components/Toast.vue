<template>
  <div class="toast" role="alert" aria-live="polite" aria-atomic="true">
    <div class="toast-header">
      <strong class="me-auto">{{ title }}</strong>
      <small>только что</small>
      <button
        type="button"
        class="btn-close"
        data-bs-dismiss="toast"
        aria-label="Close"
      ></button>
    </div>
    <div class="toast-body">
      {{ text }}
    </div>
  </div>
</template>

<script>
export default {
  props: ["text", "title"],
  mounted() {},
  data() {
    return {
      toast: null,
      alertpush: false,
    };
  },
};
</script>
