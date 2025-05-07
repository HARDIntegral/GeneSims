use plotters::prelude::*;
use plotters_canvas::CanvasBackend;
use yew::prelude::*;
use yew_router::prelude::*;

use crate::routes::Route;

#[derive(Properties, PartialEq)]
pub struct LayoutProps {
    pub title: AttrValue,
    pub children: Children,
    #[prop_or_default]
    pub graph_type: Option<GraphType>,
    #[prop_or_default]
    pub x_label: Option<String>,
    #[prop_or_default]
    pub y_label: Option<String>,
    #[prop_or_default]
    pub graph_caption: Option<String>,
    #[prop_or_default]
    pub min_y: Option<f64>,
}

#[derive(Clone, PartialEq)]
pub enum GraphType {
    MultiLineGraph(Vec<Vec<f64>>),
    Histogram(Vec<f64>),
}

#[function_component(Layout)]
pub fn layout(props: &LayoutProps) -> Html {
    {
        let graph_type = props.graph_type.clone();

        let x_label = props.x_label.clone().unwrap_or("Generations".into());
        let y_label = props.y_label.clone().unwrap_or("Allele Frequency".into());
        let caption = props
            .graph_caption
            .clone()
            .unwrap_or("Allele Frequency over Time".into());
        let min_y = props.min_y.unwrap_or(0.0);

        use_effect_with_deps(
            move |_| {
                if let Some(graph) = graph_type {
                    let backend = CanvasBackend::new("layout-graph").expect("Canvas not found");
                    let root = backend.into_drawing_area();
                    root.fill(&WHITE).unwrap();

                    match graph {
                        GraphType::MultiLineGraph(runs) => {
                            let max_gen = runs.iter().map(|r| r.len()).max().unwrap_or(50) as i32; // default to 50
                            let max_gen = max_gen.max(50); // always at least 50
                            let max_freq = 1.0;

                            let mut chart = ChartBuilder::on(&root)
                                .margin(20)
                                .caption(caption, ("sans-serif", 24))
                                .x_label_area_size(60)
                                .y_label_area_size(60)
                                .build_cartesian_2d(0..max_gen, min_y..max_freq)
                                .unwrap();

                            chart
                                .configure_mesh()
                                .x_desc(x_label)
                                .y_desc(y_label)
                                .axis_desc_style(("sans-serif", 18))
                                .light_line_style(&WHITE.mix(0.0))
                                .draw()
                                .unwrap();

                            // ✅ Only draw lines if there’s data
                            for (i, run) in runs.iter().enumerate() {
                                if run.is_empty() {
                                    continue; // skip empty runs (just keep the empty axes)
                                }
                                let color = Palette99::pick(i).mix(0.9);
                                chart
                                    .draw_series(LineSeries::new(
                                        run.iter().enumerate().map(|(i, &y)| (i as i32, y)),
                                        ShapeStyle::from(color).stroke_width(3),
                                    ))
                                    .unwrap();
                            }
                        }

                        GraphType::Histogram(data) => {
                            let max_count = *data
                                .iter()
                                .max_by(|a, b| a.partial_cmp(b).unwrap())
                                .unwrap_or(&0.0) as i32;

                            let mut chart = ChartBuilder::on(&root)
                                .margin(20)
                                .caption("Allele Frequency Distribution", ("sans-serif", 24))
                                .x_label_area_size(60)
                                .y_label_area_size(70)
                                .build_cartesian_2d(0.0..1.0, 0.0..(max_count as f64))
                                .unwrap();

                            chart
                                .configure_mesh()
                                .x_desc("Frequency of Allele p in Populations")
                                .y_desc("Number of Populations")
                                .axis_desc_style(("sans-serif", 18))
                                .light_line_style(&WHITE.mix(0.0))
                                .draw()
                                .unwrap();

                            chart
                                .draw_series(data.iter().enumerate().map(|(i, &count)| {
                                    let bin_width = 1.0 / data.len() as f64;
                                    let x0 = i as f64 * bin_width;
                                    let x1 = x0 + bin_width;
                                    Rectangle::new([(x0, 0.0), (x1, count as f64)], BLUE.filled())
                                }))
                                .unwrap();
                        }
                    }
                }

                || ()
            },
            props.graph_type.clone(),
        );
    }

    html! {
        <div>
            <header class="bg-gray-100 p-6 shadow-sm text-center">
                <h1 class="text-[36px] font-bold text-blue-700">{ "GeneSims" }</h1>
            </header>

            <nav class="bg-blue-600 text-white p-4 shadow-md">
                <ul class="flex gap-4 justify-center">
                    <li>
                        <Link<Route> to={Route::Home} classes="px-4 py-2 rounded hover:bg-blue-700 transition">
                            { "Home" }
                        </Link<Route>>
                    </li>
                    <li>
                        <Link<Route> to={Route::Drift} classes="px-4 py-2 rounded hover:bg-blue-700 transition">
                            { "Simple Drift" }
                        </Link<Route>>
                    </li>
                    <li>
                        <Link<Route> to={Route::DriftMig} classes="px-4 py-2 rounded hover:bg-blue-700 transition">
                            { "Drift With Migration" }
                        </Link<Route>>
                    </li>
                    <li>
                        <Link<Route> to={Route::DriftMut} classes="px-4 py-2 rounded hover:bg-blue-700 transition">
                            { "Drift With Mutation" }
                        </Link<Route>>
                    </li>
                    <li>
                        <Link<Route> to={Route::Selection} classes="px-4 py-2 rounded hover:bg-blue-700 transition">
                            { "Simple Selection" }
                        </Link<Route>>
                    </li>
                    <li>
                        <Link<Route> to={Route::SelecDrift} classes="px-4 py-2 rounded hover:bg-blue-700 transition">
                            { "Selection With Drift" }
                        </Link<Route>>
                    </li>
                    <li>
                        <Link<Route> to={Route::WBar} classes="px-4 py-2 rounded hover:bg-blue-700 transition">
                            { "W Bar" }
                        </Link<Route>>
                    </li>
                </ul>
            </nav>

            <div class="flex justify-center">
                <h2 class="text-xl font-semibold text-blue-700 mt-6">{ &props.title }</h2>
            </div>

            {
                if props.graph_type.is_some() {
                    html! {
                        <div class="border-2 border-blue-600 rounded-xl mx-6 mt-6 mb-0 p-6 shadow-md bg-white mt-4 center">
                            <div class="flex justify-center">
                                   <canvas id="layout-graph" width="800" height="500" class="mx-auto"></canvas>
                            </div>
                        </div>
                    }
                } else {
                    html! {}
                }
            }

            <main class="p-6">
                { for props.children.iter() }
            </main>

            <footer class="bg-gray-100 p-6 shadow-sm text-center">
                <p>{ "GeneSims created by Mohammed Tazwar ©2025, University of Georgia" }</p>
            </footer>
        </div>
    }
}
