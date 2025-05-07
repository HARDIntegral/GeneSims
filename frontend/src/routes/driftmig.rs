use crate::layout::{GraphType, Layout};
use rand::distributions::Distribution;
use rand_distr::Binomial;
use yew::prelude::*;

#[yew::function_component(DriftMig)]
pub fn drift_with_migration() -> Html {
    let population_size = use_state(|| 25);
    let migration_rate = use_state(|| 0.0);
    let populations = use_state(|| None::<Vec<f64>>);
    let histogram_data = use_state(|| vec![0.0; 10]);
    let generation = use_state(|| 0);

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
            let parsed = if val == "None" {
                0.0
            } else {
                val.parse::<f64>().unwrap_or(0.0)
            };
            state.set(parsed);
        })
    };

    let on_pop_size_change = make_usize_select_callback(population_size.clone());
    let on_mig_rate_change = make_f64_select_callback(migration_rate.clone());

    let on_step = {
        let population_size = *population_size;
        let migration_rate = *migration_rate;
        let populations = populations.clone();
        let histogram_data = histogram_data.clone();
        let generation = generation.clone();

        Callback::from(move |_| {
            let mut rng = rand::thread_rng();
            let migrant_freq = 0.5; // fixed migrant pool frequency

            let mut new_pops = if let Some(pops) = (*populations).clone() {
                pops
            } else {
                // First click: initialize 100 pops at 0.5
                vec![0.5; 100]
            };

            // Step each population
            for p in new_pops.iter_mut() {
                // Migration
                let p_mig = (1.0 - migration_rate) * (*p) + migration_rate * migrant_freq;
                // Drift
                let bin = Binomial::new(population_size as u64, p_mig).unwrap();
                let successes = bin.sample(&mut rng);
                *p = successes as f64 / population_size as f64;
            }

            // Count into 10 bins (0.0 to 1.0)
            let mut counts = vec![0.0; 10];
            for &p in new_pops.iter() {
                let bin_idx = (p * 10.0).floor() as usize;
                let idx = if bin_idx >= 10 { 9 } else { bin_idx };
                counts[idx] += 1.0;
            }

            populations.set(Some(new_pops));
            histogram_data.set(counts);
            generation.set(*generation + 1);
        })
    };

    let on_clear = {
        let populations = populations.clone();
        let histogram_data = histogram_data.clone();
        let generation = generation.clone();

        Callback::from(move |_| {
            populations.set(None);
            histogram_data.set(vec![0.0; 10]);
            generation.set(0);
        })
    };

    // Dropdown options
    let pop_options = vec![25, 100, 250];
    let mig_options = vec![
        "None".to_string(),
        "0.001".to_string(),
        "0.01".to_string(),
        "0.1".to_string(),
    ];

    html! {
        <Layout title="Drift with Migration"
            graph_type={Some(GraphType::Histogram((*histogram_data).clone()))}
        >
            <div class="border-2 border-blue-600 rounded-xl p-6 shadow-md bg-white grid grid-cols-2 gap-4">
                <div>
                    <label class="block mb-2 font-semibold">{"Population Size:"}</label>
                    <select onchange={on_pop_size_change} class="border rounded p-2 w-full bg-blue-300">
                        { for pop_options.iter().map(|&val| {
                            html! {
                                <option value={val.to_string()} selected={*population_size == val}>{ val }</option>
                            }
                        })}
                    </select>
                </div>

                <div>
                    <label class="block mb-2 font-semibold">{"Migration Rate:"}</label>
                    <select onchange={on_mig_rate_change} class="border rounded p-2 w-full bg-blue-300">
                        { for mig_options.iter().map(|val| {
                            let parsed_val = if val == "None" { 0.0 } else { val.parse::<f64>().unwrap_or(0.0) };
                            html! {
                                <option value={val.to_string()} selected={*migration_rate == parsed_val}>{ val }</option>
                            }
                        })}
                    </select>
                </div>

                <div class="flex gap-4 items-center col-span-2">
                    <button onclick={on_step} class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">{"Step"}</button>
                    <button onclick={on_clear} class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">{"Clear"}</button>
                    <span class="font-semibold">{"Generation: "} { *generation }</span>
                </div>
            </div>
        </Layout>
    }
}
