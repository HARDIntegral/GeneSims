use actix_files::Files;
use actix_web::{web, App, HttpServer, Result};

// This handles fallback for SPA routes
async fn fallback() -> Result<actix_files::NamedFile> {
    Ok(actix_files::NamedFile::open("./static/index.html")?)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let port = std::env::var("PORT").unwrap_or_else(|_| "10000".to_string());
    HttpServer::new(|| {
        App::new()
            .service(Files::new("/", "./static").index_file("index.html"))
            .default_service(web::get().to(fallback))
    })
    .bind(format!("0.0.0.0:{}", port))?
    .run()
    .await
}
