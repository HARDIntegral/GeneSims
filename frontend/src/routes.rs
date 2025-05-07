use yew::prelude::*;
use yew_router::prelude::*;

use crate::layout::Layout;

mod drift;
mod driftmig;
mod driftmut;
mod selecdrift;
mod selection;
mod wbar;

use drift::Drift;
use driftmig::DriftMig;
use driftmut::DriftMut;
use selecdrift::SelecDrift;
use selection::Selection;
use wbar::WBar;

// 🔗 Define your routes
#[derive(Clone, Routable, PartialEq)]
pub enum Route {
    #[at("/")]
    Home,
    #[at("/simple_drift")]
    Drift,
    #[at("/drift_migration")]
    DriftMig,
    #[at("/drift_mutation")]
    DriftMut,
    #[at("/selection")]
    Selection,
    #[at("/selection_with_drift")]
    SelecDrift,
    #[at("/wbar")]
    WBar,
    #[not_found]
    #[at("/404")]
    NotFound,
}

#[function_component(Home)]
pub fn home() -> Html {
    html! {
        <Layout title="Welcome To GeneSims!">
            <div class="justify-center mx-8 border-2 border-blue-600 rounded-xl p-6 shadow-md bg-white gap-4">
                <p class="pb-4">{ "GeneSims is an interactive web-based toolkit designed to model key processes in population genetics, including " } <strong> { "genetic drift" }</strong>{ ", " } <strong>{ "natural selection" }</strong>{ ", " }<strong>{ "mutation" }</strong>{ ", and " }<strong>{ "migration" }</strong>{ ". These simulations allow users to visualize how allele frequencies change over time under different evolutionary pressures in a controlled and customizable environment." }</p>
                <p>{ "The app provides several modules:" }</p>
                <ul class="pl-4">
                    <li><strong>{ "Simple Drift:" }</strong>{ " Models random changes in allele frequencies due to sampling error in small populations."}</li>
                    <li><strong>{ "Drift with Migration:" }</strong>{ " Simulates gene flow between populations, showing how migration rates influence genetic diversity." }</li>
                    <li><strong>{ "Drift with Mutation:" }</strong>{ " Explores the role of mutation in introducing new alleles and maintaining variation over generations." }</li>
                    <li><strong>{ "Simple Selection:" }</strong>{ " Demonstrates how selection coefficients affect allele frequency trajectories based on relative fitness values." }</li>
                    <li><strong>{ "Selection with Drift:" }</strong>{ " Combines natural selection and stochastic drift, offering a more realistic glimpse of evolution in finite populations." }</li>
                    <li><strong>{" W Bar:" }</strong>{ " Visualizes the population mean fitness "} <span style="text-decoration: overline">{ "𝑤" }</span> { " across allele frequency ranges, helping users understand how selection shapes fitness landscapes." }</li>
                </ul>

                <p class="pt-4">{ "Each module features real-time plotting with interactive controls, enabling users to step through generations, adjust parameters, and compare multiple simulation runs side-by-side. Whether you're a student, educator, or researcher, GeneSims provides an intuitive way to grasp the dynamic forces that shape genetic variation within populations." }</p>
            </div>
        </Layout>
    }
}

// 🚦 The router switch function
pub fn switch(routes: Route) -> Html {
    match routes {
        Route::Home => html! { <Home /> },
        Route::Drift => html! { <Drift /> },
        Route::DriftMig => html! { <DriftMig /> },
        Route::DriftMut => html! { <DriftMut /> },
        Route::Selection => html! { <Selection /> },
        Route::SelecDrift => html! { <SelecDrift /> },
        Route::WBar => html! { <WBar /> },
        Route::NotFound => html! { <h1>{ "404 - Page Not Found" }</h1> },
    }
}
