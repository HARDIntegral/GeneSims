use actix_files::Files;
use actix_web::{web, App, HttpServer, Result};

// This handles fallback for SPA routes
async fn fallback() -> Result<actix_files::NamedFile> {
    Ok(actix_files::NamedFile::open("./static/index.html")?)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(Files::new("/", "./static").index_file("index.html"))
            .default_service(web::get().to(fallback))
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
