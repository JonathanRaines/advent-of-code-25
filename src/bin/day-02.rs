use std::env;
use std::fs;
use std::ops::Range;
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

fn parse_range(range_str: &str) -> Range<usize> {
    let (min_str, max_str) = range_str.split_once("-").unwrap();
    let min = min_str.trim().parse().unwrap_or(0);
    let max = max_str.trim().parse().unwrap_or(0);
    return min..max;
}

fn find_repeats(range: &Range<usize>) -> Vec<usize> {
    let clipped_range = clip_range(range);
    if clipped_range.start == clipped_range.end {
        return vec![];
    }
    println!("{:?} -> {:?}", range, clipped_range);
    let len_sub_code: u32 = (clipped_range.start.checked_ilog10().unwrap() + 1) / 2;
    let base = BASE.pow(len_sub_code) + 1;
    let mut root = clipped_range.start / (base - 1);
    println!("Base: {}, root {}", base, root);
    let mut repeat = root * base;
    let mut repeats = Vec::new();
    while repeat <= clipped_range.end {
        if clipped_range.contains(&repeat) {
            repeats.push(repeat);
        }
        root += 1;
        repeat = root * base;
    }
    println!("{:?}", repeats);
    return repeats;
}

fn clip_range(range: &Range<usize>) -> Range<usize> {
    // Clips a range to even numbered digits
    // E.g. 123..1500 -> 1000..1500
    // This is useful because there can be no repeat codes in 123..999
    let start_digits: u32 = range.start.checked_ilog10().unwrap() + 1;
    let end_digits: u32 = range.end.checked_ilog10().unwrap() + 1;
    return Range {
        start: if start_digits & 1 == 0 {
            range.start
        } else {
            // Clip up to nearest power of 10
            BASE.pow(start_digits)
        },
        end: if end_digits & 1 == 0 {
            range.end
        } else {
            // Clip down to nearest even power of 10
            BASE.pow(end_digits - 1)
        },
    };
}
