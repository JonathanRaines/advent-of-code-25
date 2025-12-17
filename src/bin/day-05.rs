use std::env;
use std::fs;
use std::ops::RangeInclusive;
use std::process;

fn main() {
    // Parse args
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <file_path>", args[0]);
        process::exit(1);
    }

    // Read file
    let file_path = &args[1];
    let content = match fs::read_to_string(file_path) {
        Ok(data) => data,
        Err(e) => {
            eprintln!("Error reading file {}: {}", file_path, e);
            process::exit(1);
        }
    };

    // Split at the blank line
    let (ranges_str, ids_str) = match content.split_once("\n\n") {
        Some(split) => split,
        None => {
            eprintln!("Could not split the input file into ranges and ids.");
            process::exit(1);
        }
    };

    // Parse ranges
    let fresh_ranges: Vec<RangeInclusive<usize>> = match ranges_str
        .lines()
        .map(parse_range)
        .collect::<Result<Vec<_>>>()
    {
        Ok(ranges) => ranges,
        Err(e) => {
            eprintln!("Error parsing ranges: {}", e);
            process::exit(1);
        }
    };
    println!("Ranges:\n{:?}", fresh_ranges);

    // Parse ids
    let ids: Vec<usize> = match ids_str
        .lines()
        .map(|s| s.parse())
        .collect::<std::result::Result<Vec<_>, _>>()
    {
        Ok(ids) => ids,
        Err(e) => {
            eprintln!("Error parsing ids: {}", e);
            process::exit(1);
        }
    };
    println!("ids: {:?}", ids);

    let part = args.get(2).map(|s| s.as_str()).unwrap_or("1");
    match part {
        "1" => part_1(fresh_ranges, ids),
        "2" => part_2(fresh_ranges),
        _ => {
            eprintln!("Please provide an part 1 or 2");
            process::exit(1);
        }
    }
}

fn part_1(fresh_ranges: Vec<RangeInclusive<usize>>, ids: Vec<usize>) {
    let mut n_fresh: usize = 0;
    for id in ids {
        for range in &fresh_ranges {
            if !range.contains(&id) {
                continue;
            }
            n_fresh += 1;
            break;
        }
    }
    println!("Number of fresh IDs: {}", n_fresh);
}

fn part_2(fresh_ranges: Vec<RangeInclusive<usize>>) {
    // Want to avoid enumerating large ranges.
    // Can do so by doing end-start but our ranges overlap so fix that first.
    // Start by sorting ranges by start
    let mut sorted = fresh_ranges.clone();
    sorted.sort_by_key(|rng| *rng.start());
    println!("sorted: {:?}", sorted);

    // Create a new vec to put our non-overlapping ranges in.
    let mut merged: Vec<RangeInclusive<usize>> = Vec::new();
    for rng in sorted {
        // Attempt to access last element in merged.
        if let Some(last) = merged.last_mut() {
            // If non-overlapping can append it as is
            if rng.start() > last.end() {
                merged.push(rng)
            // otherwise don't add the current one at all, adjust the last added to merged.
            // The start will be the same, but the new ranges end if they just overlap,
            // or the old ranges end if the new range is a subset of the previous.
            } else {
                *last = *last.start()..=*rng.end().max(last.end())
            }
        // Or add the first from sorted.
        } else {
            merged.push(rng)
        }
    }
    println!("merged: {:?}", merged);

    let n_fresh = merged
        .iter()
        .fold(0, |acc, r| acc + r.end() + 1 - r.start());

    println!("Number of fresh IDs: {}", n_fresh);
}

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;
fn parse_range(range_str: &str) -> Result<RangeInclusive<usize>> {
    match range_str.split_once("-") {
        Some((start, end)) => Ok(start.parse::<usize>()?..=end.parse::<usize>()?),
        None => Err("Invalid range format".into()),
    }
}
