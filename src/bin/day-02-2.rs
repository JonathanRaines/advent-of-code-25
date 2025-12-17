use std::env;
use std::fs;
use std::ops::RangeInclusive;
use std::process;

const BASE: usize = 10;

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

    let ranges = content.split(",").map(parse_range);
    let repeats = ranges
        .flat_map(|range| find_repeats(&range))
        .collect::<Vec<_>>();
    let answer: usize = repeats.iter().sum();
    println!("Answer: {}", answer);
}

fn parse_range(range_str: &str) -> RangeInclusive<usize> {
    let (min_str, max_str) = range_str.split_once("-").unwrap();
    let min = min_str.trim().parse().unwrap_or(0);
    let max = max_str.trim().parse().unwrap_or(0);
    return min..=max;
}

fn find_repeats(range: &RangeInclusive<usize>) -> Vec<usize> {
    let code_len: u32 = range.end().checked_ilog10().unwrap() + 1;
    let mut sub_code_lens: Vec<u32> = Vec::new();
    for l in 2..=code_len {
        if code_len % l == 0 {
            sub_code_lens.push(code_len / l);
        }
    }
    let bases = sub_code_lens
        .iter()
        .map(|i| BASE.pow(*i) + 1)
        .collect::<Vec<_>>();
    println!("Range: {:?}, Bases: {:?}", range, bases);
    let repeats = bases
        .iter()
        .flat_map(|base| find_repeats_for_base(&range, &base));
    return repeats.collect();
}

fn find_repeats_for_base(range: &RangeInclusive<usize>, base: &usize) -> Vec<usize> {
    let mut root = range.start() / base;
    let mut repeat = root * base;
    let mut repeats = Vec::new();
    while &repeat <= range.end() {
        if range.contains(&repeat) {
            repeats.push(repeat);
        }
        root += 1;
        repeat = root * base;
    }
    println!("{:?}, base: {}, {:?}", range, base, repeats);
    return repeats;
}
