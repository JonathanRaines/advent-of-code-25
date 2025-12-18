use std::env;
use std::fs;
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

    let part = args.get(2).map(|s| s.as_str()).unwrap_or("1");
    match part {
        "1" => part_1(content),
        "2" => part_2(content),
        _ => {
            eprintln!("Please provide an part 1 or 2");
            process::exit(1);
        }
    };
}

fn part_1(content: String) {
    let width = content.lines().next().unwrap().len();
    let mut tachyons: Vec<bool> = vec![false; width];
    let mut split_count = 0;
    for line in content.lines() {
        for (i, c) in line.chars().enumerate() {
            match c {
                'S' => tachyons[i] = true,
                '^' => {
                    if tachyons[i] {
                        tachyons[i] = false;
                        tachyons.get_mut(i + 1).map(|x| *x = true);
                        tachyons.get_mut(i - 1).map(|x| *x = true);
                        split_count += 1;
                    }
                }
                _ => {}
            }
        }
    }
    println!("Splits: {}", split_count)
}

fn part_2(content: String) {
    let width = content.lines().next().unwrap().len();
    let mut tachyons: Vec<u64> = vec![0; width];
    let mut split_count = 0;
    for line in content.lines() {
        for (i, c) in line.chars().enumerate() {
            match c {
                'S' => tachyons[i] = 1,
                '^' => {
                    if tachyons[i] > 0 {
                        let current_tachyons = tachyons[i];
                        tachyons.get_mut(i + 1).map(|x| *x += current_tachyons);
                        tachyons.get_mut(i - 1).map(|x| *x += current_tachyons);
                        tachyons[i] = 0;
                        split_count += 1;
                    }
                }
                _ => {}
            }
        }
    }
    println!("Splits: {}", split_count);
    println!("Total timelines: {}", tachyons.iter().sum::<u64>());
}
