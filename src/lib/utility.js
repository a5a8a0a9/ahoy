export const UtilityMixin = {
  methods: {
    /**
     * 將卷軸移至某個元素
     * @param {Element} el - DOM 元素
     * @param {Object} shiftCorrect - 元素移動位置的修正量
     * @param {Object} offsetType - 移動方式
     * @param {String} behavior - scrollToInfo({ behavior })
     */
    scrollToEl(
      el,
      shiftCorrect = { x: 0, y: 0 },
      offsetType = { x: "left", y: "top" },
      behavior = "smooth"
    ) {
      if (el === null) {
        return;
      }
      shiftCorrect = {
        x: shiftCorrect.x || 0,
        y: shiftCorrect.y || 0,
      };
      offsetType = {
        x: offsetType.x || "left",
        y: offsetType.y || "top",
      };
      const elRect = el.getBoundingClientRect();

      if (el.horizontalScrollElement) {
        const scrollEl = el.horizontalScrollElement;
        const scrollElRect = scrollEl.getBoundingClientRect();
        switch (offsetType.x) {
          case "left":
            scrollEl.scrollTo({
              left:
                scrollEl.scrollLeft -
                scrollElRect.x +
                elRect.x +
                shiftCorrect.x,
              behavior,
            });
            break;
          case "center": {
            const scrollZeroingX = scrollEl.scrollLeft - scrollElRect.x;
            const scrollCenterX = scrollZeroingX - scrollElRect.width / 2;
            const elCenterX = elRect.x + elRect.width / 2;
            scrollEl.scrollTo({
              left: scrollCenterX + elCenterX,
              behavior,
            });
            break;
          }
        }
      }

      if (el.verticalScrollElement) {
        const scrollEl = el.verticalScrollElement;
        const scrollElRect = scrollEl.getBoundingClientRect();
        switch (offsetType.y) {
          case "top":
            scrollEl.scrollTo({
              top:
                scrollEl.scrollTop - scrollElRect.y + elRect.y + shiftCorrect.y,
              behavior,
            });
            break;
          case "center": {
            const scrollZeroingY = scrollEl.scrollTop - scrollElRect.y;
            const scrollCenterY = scrollZeroingY - scrollElRect.height / 2;
            const elCenterY = elRect.y + elRect.height / 2;
            scrollEl.scrollTo({
              top: scrollCenterY + elCenterY,
              behavior,
            });
            break;
          }
        }
      }
    },
    onCopySuccess(e) {
      alert(`已複製：${e.text}`);
    },
    onCopyError(e) {
      alert("copy error", e);
    },
    /***
     *
      <input v-model="test" />
      <button
        v-clipboard:copy="test"
        v-clipboard:success="onCopySuccess"
        v-clipboard:error="onCopyError"
      >
        copy
      </button>
     */
    doCopy(text) {
      this.$copyText(text)
        .then((e) => {
          this.onCopySuccess(e);
        })
        .catch((e) => {
          this.onCopyError(e);
        });
    },
  },
};

export default {
  install(Vue) {
    Vue.mixin(UtilityMixin);
  },
};
