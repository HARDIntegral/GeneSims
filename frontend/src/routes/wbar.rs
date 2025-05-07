use crate::layout::{GraphType, Layout};
use yew::prelude::*;

#[yew::function_component(WBar)]
pub fn wbar() -> Html {
    let w11 = use_state(|| 1.0);
    let w12 = use_state(|| 1.0);
    let w22 = use_state(|| 1.0);
    let graph_data = use_state(|| vec![]); // Vec<Vec<f64>>

    let make_f64_select_callback = |state: UseStateHandle<f64>| {
        Callback::from(move |e: Event| {
            let val = e
                .target_unchecked_into::<web_sys::HtmlSelectElement>()
                .value();
            if let Ok(parsed) = val.parse::<f64>() {
                state.set(parsed);
            }
        })
    };

    let on_w11_change = make_f64_select_callback(w11.clone());
    let on_w12_change = make_f64_select_callback(w12.clone());
    let on_w22_change = make_f64_select_callback(w22.clone());

    let on_start = {
        let w11 = *w11;
        let w12 = *w12;
        let w22 = *w22;
        let graph_data = graph_data.clone();

        Callback::from(move |_| {
            let result = generate_wbar_curve(w11, w12, w22);

            let mut new_data = (*graph_data).clone();
            new_data.push(result);

            graph_data.set(new_data);
        })
    };

    let on_clear = {
        let graph_data = graph_data.clone();
        Callback::from(move |_| {
            graph_data.set(vec![]);
        })
    };

    let fitness_options = vec![1.0, 0.9, 0.8, 0.7, 0.6];

    html! {
        <Layout title="W Bar"
            graph_type={
                if graph_data.is_empty() {
                    // Default empty graph with one blank line to keep axes up
                    Some(GraphType::MultiLineGraph(vec![vec![]]))
                } else {
                    Some(GraphType::MultiLineGraph((*graph_data).clone()))
                }
            }
            x_label={"Allele Frequency as a Percentage".to_string()}
            y_label={"W Bar".to_string()}
            graph_caption={"W Bar Value over Allele Frequency".to_string()}
            min_y={0.5}

        >
            <div class="border-2 border-blue-600 rounded-xl p-6 shadow-md bg-white grid grid-cols-3 gap-4">
                <div>
                    <label class="block mb-2 font-semibold">{"w11:"}</label>
                    <select onchange={on_w11_change} class="border rounded p-2 w-full bg-blue-300">
                        { for fitness_options.iter().map(|&val| {
                            html! {
                                <option value={val.to_string()} selected={*w11 == val}>{ val }</option>
                            }
                        })}
                    </select>
                </div>
                <div>
                    <label class="block mb-2 font-semibold">{"w12:"}</label>
                    <select onchange={on_w12_change} class="border rounded p-2 w-full bg-blue-300">
                        { for fitness_options.iter().map(|&val| {
                            html! {
                                <option value={val.to_string()} selected={*w12 == val}>{ val }</option>
                            }
                        })}
                    </select>
                </div>
                <div>
                    <label class="block mb-2 font-semibold">{"w22:"}</label>
                    <select onchange={on_w22_change} class="border rounded p-2 w-full bg-blue-300">
                        { for fitness_options.iter().map(|&val| {
                            html! {
                                <option value={val.to_string()} selected={*w22 == val}>{ val }</option>
                            }
                        })}
                    </select>
                </div>

                <div class="flex gap-4 items-end col-span-3">
                    <button onclick={on_start} class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">{"Start"}</button>
                    <button onclick={on_clear} class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">{"Clear"}</button>
                </div>
            </div>
        </Layout>
    }
}

// --- W Bar curve generator ---
fn generate_wbar_curve(w11: f64, w12: f64, w22: f64) -> Vec<f64> {
    let steps = 100;
    let mut curve = vec![];

    for i in 0..=steps {
        let p = i as f64 / steps as f64;
        let w_bar = p * p * w11 + 2.0 * p * (1.0 - p) * w12 + (1.0 - p) * (1.0 - p) * w22;
        curve.push(w_bar);
    }

    curve
}
