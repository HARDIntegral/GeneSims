# GeneSims

### Welcome To [GeneSims](https://genesims.onrender.com)!

GeneSims is an interactive web-based toolkit designed to model key processes in population genetics, including **genetic drift**, **natural selection**, **mutation**, and **migration**. These simulations allow users to visualize how allele frequencies change over time under different evolutionary pressures in a controlled and customizable environment.

The app provides several modules:

- **Simple Drift:** Models random changes in allele frequencies due to sampling error in small populations.
- **Drift with Migration:** Simulates gene flow between populations, showing how migration rates influence genetic diversity.
- **Drift with Mutation:** Explores the role of mutation in introducing new alleles and maintaining variation over generations.
- **Simple Selection:** Demonstrates how selection coefficients affect allele frequency trajectories based on relative fitness values.
- **Selection with Drift:** Combines natural selection and stochastic drift, offering a more realistic glimpse of evolution in finite populations.
- **W Bar:** Visualizes the population mean fitness 𝑤 bar across allele frequency ranges, helping users understand how selection shapes fitness landscapes.

Each module features real-time plotting with interactive controls, enabling users to step through generations, adjust parameters, and compare multiple simulation runs side-by-side. Whether you're a student, educator, or researcher, GeneSims provides an intuitive way to grasp the dynamic forces that shape genetic variation within populations.

### How To Build The Project Yourself

The only dependency required for this application that needs to be installed manually is cargo and can be installed by:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
and you can test the installation by running:
```bash
cargo --version
```


Clone the repo:
```bash
git clone https://github.com/HARDIntegral/GeneSims.git
cd GeneSims
```

Build the static site:
```bash
cd frontend
trunk build --release --dist ../backend/static
```

Build the Actix backend
```bash
cd ../backend
cargo build --release
```
Note: if you are running the site locally, change the ip address from `0.0.0.0` to `127.0.0.1` and set a desired port value.
