var gulp = require('gulp'),
    gutil = require('gulp-util'),
    sass = require('gulp-sass'),
    browserSync = require('browser-sync'),
    concat = require('gulp-concat'),
    uglify = require('gulp-uglify'),
    cleanCSS = require('gulp-clean-css'),
    rename = require('gulp-rename'),
    del = require('del'),
    imagemin = require('gulp-imagemin'),
    cache = require('gulp-cache'),
    autoprefixer = require('gulp-autoprefixer'),
    notify = require("gulp-notify"),
    htmlmin = require('gulp-htmlmin');

// Скрипты проекта

gulp.task('common-js', function () {
    return gulp.src([
        'app/js/common.js'
    ])
        .pipe(concat('common.min.js'))
        //.pipe(uglify())
        .pipe(gulp.dest('app/js'));
});


gulp.task('js', ['common-js'], function () {
    return gulp.src([
        'app/libs/jquery/dist/jquery.min.js',
        'app/libs/jquery/dist/newWaterfall.js',
        'app/libs/semantic/dist/semantic.min.js',
        'app/libs/masked-input/jquery.mask.min.js',
        'app/libs/unite_gallery/js/unitegallery.min.js',
        'app/libs/unite_gallery/themes/default/ug-theme-default.js',
        'app/libs/stickyjs/sticky.min.js',
        // 'app/libs/dropzone/dropzone.js',
        // 'app/libs/dropzone/dropzone-amd-module.js',
        'app/js/common.min.js'
    ])
        .pipe(concat('scripts.v1.9.min.js'))
        //.pipe(uglify()) // Минимизировать весь js (на выбор)
        .pipe(gulp.dest('../static/js'));
});


gulp.task('browser-sync', function () {
    browserSync.init({
        notify: false,
        proxy: "127.0.0.1:8000"
    });
});

gulp.task('sass', function () {
    return gulp.src('app/sass/**/*.sass')
        .pipe(sass({outputStyle: 'expand'}).on("error", notify.onError()))
        .pipe(rename({suffix: '.min', prefix: ''}))
        .pipe(autoprefixer(['last 15 versions']))
        .pipe(cleanCSS()) // Опционально, закомментировать при отладке
        .pipe(gulp.dest('app/css'))
        .pipe(gulp.dest('../static/css'));
});

gulp.task('html', function () {
    return gulp.src(['app/**/*.html'])
        .pipe(htmlmin({
            collapseWhitespace: true,
            ignoreCustomFragments: [ /<%[\s\S]*?%>/, /<\?[\s\S]*?\?>/, /{({|%).*?(}|%)}/],
            removeComments: true,
            minifyCSS: true
        }))
        .pipe(gulp.dest('../templates'));
});

gulp.task('watch', ['js', 'sass', 'html', 'browser-sync'], function () {
    gulp.watch(['app/**/*.html'], ['html', browserSync.reload]);
    gulp.watch(['app/js/common.js'], ['common-js', browserSync.reload]);
    gulp.watch(['app/sass/**/*.sass'], ['sass', browserSync.reload]);
    gulp.watch(['app/js/common.min.js'], ['js', browserSync.reload]);
});

gulp.task('imagemin', function () {
    return gulp.src('app/img/**/*')
        .pipe(cache(imagemin()))
        .pipe(gulp.dest('../static/img'));
});


gulp.task('clearcache', function () {
    return cache.clearAll();
});

gulp.task('default', ['watch']);
