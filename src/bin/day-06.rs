use ndarray::{Array2, Array3, Axis, array, s};
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

    let (nums_str, ops_str) = content.trim().rsplit_once("\n").unwrap();
    println!("{}", nums_str);

    let part = args.get(2).map(|s| s.as_str()).unwrap_or("1");
    let numbers = match part {
        "1" => parse_grid(nums_str),
        "2" => parse_ceph_grid(nums_str),
        _ => {
            eprintln!("Please provide an part 1 or 2");
            process::exit(1);
        }
    };
    let ops: Vec<&str> = ops_str.split_whitespace().collect();
    let mut results = Vec::new();
    for (nums, op) in numbers.iter().zip(ops) {
        match op {
            "+" => results.push(nums.iter().sum()),
            "*" => results.push(nums.iter().product()),
            _ => {
                eprintln!("Unexpected operation {}", op);
                process::exit(1);
            }
        };
    }
    println!("Numbers:\n{:?}", numbers);
    println!("Results:\n{:?}", results);
    println!("Total: {}", results.iter().sum::<u64>());
}

fn parse_grid(grid_string: &str) -> Vec<Vec<u64>> {
    let mut flat_data = Vec::new();

    let mut num_rows = 0;
    let mut num_cols = 0;

    for line in grid_string.lines() {
        if num_rows == 0 {
            num_cols = line.split_whitespace().count();
            println!("Num cols: {}", num_cols)
        }
        flat_data.extend(line.split_whitespace().map(|s| s.parse::<u64>().unwrap()));
        num_rows += 1;
    }

    let arr = Array2::from_shape_vec((num_rows, num_cols), flat_data).unwrap();

    arr.columns().into_iter().map(|col| col.to_vec()).collect()
}

fn parse_ceph_grid(grid_string: &str) -> Vec<Vec<u64>> {
    let flat_data: Vec<char> = grid_string.chars().filter(|c| c != &'\n').collect();
    let char_w = grid_string.lines().next().unwrap().chars().count();
    let n_rows = grid_string.lines().count();

    let char_grid = Array2::from_shape_vec((n_rows, char_w), flat_data).unwrap();

    let vals: Vec<u64> = char_grid
        .columns()
        .into_iter()
        .map(|col| {
            col.into_iter()
                .collect::<String>()
                .trim()
                .parse::<u64>()
                .unwrap_or(0)
        })
        .collect();

    vals.split(|i| i == &0)
        .map(|v| v.to_vec())
        .collect::<Vec<Vec<u64>>>()
}
