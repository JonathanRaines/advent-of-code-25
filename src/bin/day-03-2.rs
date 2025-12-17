use std::env;
use std::fs;
use std::process;

const BASE: u128 = 10;

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
    let max_joltages: Vec<u128> = joltages.iter().map(find_max_joltage).collect();
    let total_joltage: u128 = max_joltages.iter().sum();
    for (jolts, max) in content.lines().zip(max_joltages.iter()) {
        println!("Joltages: {:?}, Max Joltage: {}", jolts, max);
    }
    println!("Total Joltage: {}", total_joltage)
}

fn parse_bank(bank: &str) -> Vec<u32> {
    bank.chars().map(|c| c.to_digit(10).unwrap()).collect()
}

fn find_max_joltage(joltages: &Vec<u32>) -> u128 {
    // Find the least valuable 3 digits and remove them.
    let mut prev_j = joltages[0];
    let n_to_remove: usize = joltages.len() - 12;
    println!("{} {}", joltages.len(), n_to_remove);
    let mut to_remove: Vec<usize> = vec![];
    // Remove numbers that have larger numbers after them
    for (i, joltage) in joltages[1..joltages.len()].iter().enumerate() {
        if joltage >= &prev_j {
            to_remove.push(i);
        }
        prev_j = *joltage;
        if to_remove.len() == n_to_remove {
            break;
        }
    }
    println!("n_to_remove {}", to_remove.len());
    let mut jolts = joltages.clone();
    for i in to_remove.iter().rev() {
        jolts.remove(*i);
    }
    // Sum by enumerating the numbers in reverse and using their index as power 10
    // e.g. [2,1] -> 1*10^0 + 2*10^1 = 21.
    // This approach works on the example but overflows on the input.
    println!("{}", jolts.len());
    let total_jolts: u128 = jolts
        .iter()
        .rev()
        .enumerate()
        .map(|(pow, val)| BASE.pow(pow as u32) * *val as u128)
        .sum();

    return total_jolts;
}
