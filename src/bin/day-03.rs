use std::env;
use std::fs;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <file_path>", args[0]);
        process::exit(1);
    }

    let file_path = &args[1];
    let content = match fs::read_to_string(file_path) {
        Ok(data) => data,
        Err(e) => {
            eprintln!("Error reading file {}: {}", file_path, e);
            process::exit(1);
        }
    };

    let joltages: Vec<Vec<u32>> = content.lines().map(parse_bank).collect();
    let max_joltages: Vec<u32> = joltages.iter().map(find_max_joltage).collect();
    let total_joltage: u32 = max_joltages.iter().sum();
    for (jolts, max) in content.lines().zip(max_joltages.iter()) {
        println!("Joltages: {:?}, Max Joltage: {}", jolts, max);
    }
    println!("Total Joltage: {}", total_joltage)
}

fn parse_bank(bank: &str) -> Vec<u32> {
    bank.chars().map(|c| c.to_digit(10).unwrap()).collect()
}

fn find_max_joltage(joltages: &Vec<u32>) -> u32 {
    let (first_j_value, _, first_j_index) = joltages[..joltages.len() - 1]
        .iter()
        .enumerate() // (index, value)
        // Tuples sorted in order so swap value to the front.
        // Also prioritize earlier entries
        .map(|(index, value)| (value, joltages.len() - index, index))
        .max()
        .unwrap();
    let second_j = joltages[first_j_index + 1..joltages.len()]
        .iter()
        .max()
        .unwrap();
    let max_joltage: u32 = 10 * first_j_value + second_j;
    return max_joltage;
}
