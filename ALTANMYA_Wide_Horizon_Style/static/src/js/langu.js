odoo.define('ALTANMYA_Web_Fateh.carousel', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.carousel = publicWidget.Widget.extend({
        selector: '.dynamic_snippet_template',
        events: {
            'click .next-button': '_onNextButtonClick',
            'click .prev-button': '_onPrevButtonClick',
            'click .carousel-indicator': '_onIndicatorClick',
        },
        start: function () {
            this.$slides = this.$('.my-4');
            this.currentSlide = 0;
            this.showSlide(this.currentSlide);
            this._renderIndicators();
            this._renderArrows();
            this._startAutoScroll(); // Start the auto-scroll timer
            return this._super.apply(this, arguments);
        },
        showSlide: function (index) {
            this.$slides.removeClass('active-slide');
            this.$slides.eq(index).addClass('active-slide');
        },
        _onNextButtonClick: function () {
            clearInterval(this.autoScrollTimer); // Stop the auto-scroll timer
            this.currentSlide++;
            if (this.currentSlide >= this.$slides.length) {
                this.currentSlide = 0;
            }
            this.showSlide(this.currentSlide);
            this._updateIndicators();
            this._updateSlideButtons();
            this._startAutoScroll(); // Restart the auto-scroll timer
        },
        _onPrevButtonClick: function () {
            clearInterval(this.autoScrollTimer); // Stop the auto-scroll timer
            this.currentSlide--;
            if (this.currentSlide < 0) {
                this.currentSlide = this.$slides.length - 1;
            }
            this.showSlide(this.currentSlide);
            this._updateIndicators();
            this._updateSlideButtons();
            this._startAutoScroll(); // Restart the auto-scroll timer
        },
       _renderIndicators: function () {
          var indicatorsContainer = $('<div>').addClass('carousel-indicators');
          this.$el.append(indicatorsContainer);

          for (var i = 0; i < this.$slides.length; i++) {
            var indicator = $('<div>')
              .addClass('carousel-indicator')
              .attr('data-slide-index', i);

            if (i === this.currentSlide) {
              indicator.addClass('active');
            }

            indicatorsContainer.append(indicator);
          }
        },
        _updateIndicators: function () {
            var indicators = this.$('.carousel-indicator');
            indicators.removeClass('active');
            indicators.eq(this.currentSlide).addClass('active');
        },
        _renderArrows: function () {
            var prevButton = $('<a>').addClass('carousel-arrow prev-button').html('&#8249;');
            var nextButton = $('<a>').addClass('carousel-arrow next-button').html('&#8250;');
            this.$el.prepend(prevButton, nextButton);
            this._renderSlideButtons();
        },
        _renderSlideButtons: function () {
            var self = this;
            var indicatorsContainer = this.$('.carousel-indicators');
            this.$slides.each(function (index) {
                var button = $('<button>').addClass('carousel-slide-button').attr('data-slide-index', index);
                if (index === self.currentSlide) {
                    button.addClass('active');
                }
                indicatorsContainer.append(button);
            });
        },
        _onIndicatorClick: function (ev) {
          var indicator = $(ev.currentTarget);
          var index = indicator.attr('data-slide-index');

          if (index !== this.currentSlide) {
            this.currentSlide = parseInt(index);
            this.showSlide(this.currentSlide);
            this._updateIndicators();
            this._updateSlideButtons();
            clearInterval(this.autoScrollTimer);
            this._startAutoScroll();
          }
        },

        _updateSlideButtons: function () {
            var buttons = this.$('.carousel-slide-button');
            buttons.removeClass('active');
            buttons.eq(this.currentSlide).addClass('active');
        },
        _startAutoScroll: function () {
            var self = this;
            this.autoScrollTimer = setInterval(function () {
                self._onNextButtonClick();
            }, 5000); // Adjust the time interval as needed (e.g., 3000ms = 3 seconds)
        },
    });
});