function MangaReaderNetPlugin() {
}

MangaReaderNetPlugin.prototype.parseURL = function(url) {
    var parts = url.split("/").filter(function(s) { return s.length !== 0});
    var not_mangas = ["popular", "search", "alphabetical", "latest", "random"];

    if (parts.length < 1) {
        return null;
    }
    for (var i = 0; i < not_mangas.length; ++i) {
        if (parts[0] === not_mangas[i]) {
            return null;
        }
    }
    var name = parts[0];
    var chapter = null;
    var page = null;
    if (parts.length > 1) {
        chapter = parts[1];
        if (parts.length > 2) {
            page = parts[2];
        } else {
            page = 1;
        }
    }

    return { common: { name, chapter, page }};
}
