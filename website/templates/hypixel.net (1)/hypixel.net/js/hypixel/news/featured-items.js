new Vue({
    el: '.featuredItems',
    data: {
        slider: null,
        itemCount: 0,
        currentIndex: 0
    },
    mounted: function() {
        const children = this.$el.querySelectorAll('.featuredItems-item');

        this.slider = simpleslider.getSlider({
            container: this.$el,
            children: children,
            delay: 7,
            prop: 'opacity',
            unit: '',
            init: 0,
            show: 1,
            end: 0,
            onChange: this.onSliderChange
        });

        this.itemCount = children.length;
    },
    methods: {
        onSliderChange: function() {
            this.currentIndex = this.slider.currentIndex();
        },
        goTo: function(event, index) {
            event.preventDefault();

            if (this.slider == null) return;

            return this.slider.change(index);
        }
    }
});