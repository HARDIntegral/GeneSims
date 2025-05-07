use yew::prelude::*;
use yew_router::prelude::*;

mod layout;
mod routes;
use routes::{switch, Route};

#[function_component(App)]
fn app() -> Html {
    html! {
        <BrowserRouter>
            <Switch<Route> render={switch} />
        </BrowserRouter>
    }
}

fn main() {
    wasm_logger::init(wasm_logger::Config::default());
    log::info!("Starting the app");
    yew::Renderer::<App>::new().render();
}
