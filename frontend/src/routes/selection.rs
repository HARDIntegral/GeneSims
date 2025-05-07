use crate::layout::{GraphType, Layout};
use yew::prelude::*;

#[yew::function_component(Selection)]
pub fn selection() -> Html {
    // --- States ---
    let num_generations = use_state(|| 50);
    let w11 = use_state(|| 1.0);
    let w12 = use_state(|| 1.0);
    let w22 = use_state(|| 1.0);
    let initial_p = use_state(|| 0.1);
    let graph_data = use_state(|| vec![vec![]]); // starts empty
    let max_generations = use_state(|| 50);

    // --- Handlers ---
    let make_usize_select_callback = |state: UseStateHandle<usize>| {
        Callback::from(move |e: Event| {
            let val = e
                .target_unchecked_into::<web_sys::HtmlSelectElement>()
                .value();
            if let Ok(parsed) = val.parse::<usize>() {
                state.set(parsed);
            }
        })
    };

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

    let on_num_gen_change = make_usize_select_callback(num_generations.clone());
    let on_w11_change = make_f64_select_callback(w11.clone());
    let on_w12_change = make_f64_select_callback(w12.clone());
    let on_w22_change = make_f64_select_callback(w22.clone());
    let on_initial_p_change = make_f64_select_callback(initial_p.clone());

    let on_start = {
        let num_generations = *num_generations;
        let w11 = *w11;
        let w12 = *w12;
        let w22 = *w22;
        let initial_p = *initial_p;
        let graph_data = graph_data.clone();
        let max_generations = max_generations.clone();

        Callback::from(move |_| {
            let result = simulate_selection(num_generations, w11, w12, w22, initial_p);

            let mut new_data = (*graph_data).clone();
            new_data.push(result);

            if num_generations > *max_generations {
                max_generations.set(num_generations);
            }

            graph_data.set(new_data);
        })
    };

    let on_clear = {
        let graph_data = graph_data.clone();
        let max_generations = max_generations.clone();
        Callback::from(move |_| {
            graph_data.set(vec![vec![]]); // keep empty graph visible
            max_generations.set(50); // reset default
        })
    };

    // Dropdown options
    let p_options = vec![0.1, 0.5, 0.9];
    let gen_options = vec![50, 100, 500, 1000, 5000, 10000];
    let fitness_options = vec![1.0, 0.9, 0.8, 0.7, 0.6];

    html! {
        <Layout title="Simple Selection"
            graph_type={Some(GraphType::MultiLineGraph((*graph_data).clone()))}
        >
            <div class="border-2 border-blue-600 rounded-xl p-6 shadow-md bg-white grid grid-cols-3 gap-4">
                <div>
                    <label class="block mb-2 font-semibold">{"Number of Generations:"}</label>
                    <select onchange={on_num_gen_change} class="border rounded p-2 w-full bg-blue-300">
                        { for gen_options.iter().map(|&val| {
                            html! {
                                <option value={val.to_string()} selected={*num_generations == val}>{ val }</option>
                            }
                        })}
                    </select>
                </div>

                <div>
                    <label class="block mb-2 font-semibold">{"Fitness for A1A1 (w11):"}</label>
                    <select onchange={on_w11_change} class="border rounded p-2 w-full bg-blue-300">
                        { for fitness_options.iter().map(|&val| {
                            html! {
                                <option value={val.to_string()} selected={*w11 == val}>{ val }</option>
                            }
                        })}
                    </select>
                </div>

                <div>
                    <label class="block mb-2 font-semibold">{"Fitness for A1A2 (w12):"}</label>
                    <select onchange={on_w12_change} class="border rounded p-2 w-full bg-blue-300">
                        { for fitness_options.iter().map(|&val| {
                            html! {
                                <option value={val.to_string()} selected={*w12 == val}>{ val }</option>
                            }
                        })}
                    </select>
                </div>

                <div>
                    <label class="block mb-2 font-semibold">{"Fitness for A2A2 (w22):"}</label>
                    <select onchange={on_w22_change} class="border rounded p-2 w-full bg-blue-300">
                        { for fitness_options.iter().map(|&val| {
                            html! {
                                <option value={val.to_string()} selected={*w22 == val}>{ val }</option>
                            }
                        })}
                    </select>
                </div>

                <div>
                    <label class="block mb-2 font-semibold">{"Initial Allele Frequency (p):"}</label>
                    <select onchange={on_initial_p_change} class="border rounded p-2 w-full bg-blue-300">
                        { for p_options.iter().map(|&val| {
                            html! {
                                <option value={val.to_string()} selected={*initial_p == val}>{ val }</option>
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

// --- Simulation logic ---
fn simulate_selection(
    num_generations: usize,
    w11: f64,
    w12: f64,
    w22: f64,
    initial_p: f64,
) -> Vec<f64> {
    let mut p = initial_p;
    let mut frequencies = vec![p];

    for _ in 0..num_generations {
        let w_bar = p * p * w11 + 2.0 * p * (1.0 - p) * w12 + (1.0 - p) * (1.0 - p) * w22;
        p = (p * (p * w11 + (1.0 - p) * w12)) / w_bar;
        frequencies.push(p);
    }

    frequencies
}
