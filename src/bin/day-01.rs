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
    let dial_moves = match fs::read_to_string(file_path) {
        Ok(data) => data,
        Err(e) => {
            eprintln!("Error reading file {}: {}", file_path, e);
            process::exit(1);
        }
    };

    let mut prev_zero_count: usize;
    let mut zero_count: usize = 0;
    let mut prev_dial: i16;
    let mut dial: i16 = 50;

    for (i, mv) in dial_moves.lines().enumerate() {
        prev_zero_count = zero_count;
        prev_dial = dial;
        let (direction, rest) = mv.split_at(1);
        let increment = rest.trim().parse::<i16>().unwrap();
        match direction {
            "L" => dial -= increment,
            "R" => dial += increment,
            _ => {
                eprintln!("Invalid dial move {}", mv)
            }
        }
        // Get into the -99..99 range if outside using mod
        if dial < -99 || dial > 99 {
            zero_count += (dial / 100).abs() as usize;
            dial %= 100;
        }
        // Move into the 0..99 range if in -99..0
        if dial < 0 {
            dial += 100;
            // Avoid double counting in the case coming from 0
            // E.g. 0 L1 -> -1 -> 99 shouldn't get +1 because the dial move 0->99
            if prev_dial != 0 {
                zero_count += 1;
            }
        }
        // Handle landing on zero in the right circumstances
        // If direction is R, dial clocked over onto zero so already accounted for in mod
        if dial == 0 && direction != "R" && prev_dial != 0 {
            zero_count += 1;
        }
        println!(
            "{}: {} {} -> {} | {} (+{})",
            i,
            prev_dial,
            mv,
            dial,
            zero_count,
            zero_count - prev_zero_count
        );
    }
    println!("Zero count: {}", zero_count);
}
