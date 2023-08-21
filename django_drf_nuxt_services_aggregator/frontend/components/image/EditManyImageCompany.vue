<template>
  <div>
    <dropzone
      v-if="drop"
      @vdropzone-file-added="onFileAdded"
      @vdropzone-removed-file="removeFileOne"
      @vdropzone-error="onError"
      @vdropzone-success="onSuccess"
      @vdropzone-complete="onComplete"
      @vdropzone-max-files-reached="MaxFile"
      ref="DropImages"
      id="dropzone"
      :options="dropzoneOptions"
    />

    <div class="mt-4">
      <p
        style="font-weight: bold;
    color: #666666;
}"
        class="text-center"
      ></p>
    </div>
  </div>
</template>

<script>
export default {
  props: ["AddImages", "images"],
  mounted() {
    if (!process.client) return;
    this.drop = true;
    let self = this;
    // this.label_photo = this.logo_company;
    if (self.images) {
      this.dropzoneOptions.init = function () {
        var thisDropzone = this;

        for (let image of self.images) {
          console.log(image.image);
          let mockFile = {
            name: image.image,
            pk: image.id,
            size: 12,
            type: "image/jpeg",
          };
          self.onFileAdded(mockFile);
          thisDropzone.emit("addedfile", mockFile);
          thisDropzone.emit("success", mockFile);
          thisDropzone.emit("thumbnail", mockFile, image.image);
          // this.on("maxfilesexceeded", function (file) {
          //   this.removeFile(file);
          //   alert("No more files please!");
          // });
        }
      };
    }
  },
  data() {
    return {
      drop: false,
      image_name: null,
      document: false,
      label_photo: [],
      maxFiles: false,
      dropzoneOptions: {
        url: `/api/companies/images/create/${this.$route.params.id}/`,
        method: "post",
        paramName: "image_company",
        maxFiles: 8,
        autoProcessQueue: true,
        thumbnailWidth: 160,
        thumbnailHeight: 160,
        resizeWidth: 1000,
        resizeHeight: 1000,
        resizeQuality: 0.5,
        resizeMimeType: "image/jpeg",
        thumbnailMethod: "contain",
        addRemoveLinks: true,
        parallelUploads: 2,
        timeout: 120000,
        dictMaxFilesExceeded: "Достигнут лимит загрузки файлов, разрешено ",
        dictDefaultMessage:
          '<div class="d-flex align-center justify-center"><img class="mr-2" height="25p" src="/uploadimage.png" alt=""><div class="" style="font-size:16px">Перетащите фотографии компании </div></div>',
        acceptedFiles: "image/*",
        //   headers: { "My-Awesome-Header": "header value" }
      },
    };
  },
  computed: {},
  methods: {
    removeFileOne(e) {
      console.log();
      if(this.$route.params.id){
      this.OnRemoveApi(e.pk);
      }
      if (this.maxFiles) {
        this.$refs.DropImages.setupEventListeners();
      }
      console.log("one");
      this.AddImages(this.$refs.DropImages.dropzone.files);
    },
    MaxFile(file) {
      this.$refs.DropImages.removeEventListeners();
      this.maxFiles = true;
      console.log("max-file");
    },

    onFileAdded(e) {
      //   this.AddImages(this.$refs.DropImages.dropzone.files);
      //   console.log(12, e.upload.filename);
    },
    onError(e) {},
    onSuccess(e) {},
    onComplete(e) {
      try {
        document.querySelector(".dz-remove").innerHTML = "удалить";
      } catch (error) {
        console.log("error");
      }

      e.pk = JSON.parse(e.xhr.response).message;

    },
    OnRemoveApi(pk) {
      let headers = {
        "Content-Type": "application/json",
      };
      console.log("delete");
      this.$axios
        .$delete(`api/v1/companies/images/delete/${pk}/`, {
          headers: headers,
        })
        .then((resp) => {
          console.log(resp);
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  },
};
</script>
<style>
.dropzone.dz-clickable {
  font-weight: 800;
  border: 2px dotted #e5e5e5;
  background-color: #f9fafb;
  border-radius: 8px !important;

}
.vue-dropzone > .dz-preview .dz-image {
  border-radius: 0;
  width: 160px;

  height: 160px;
}
</style>
