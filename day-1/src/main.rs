use std::env;
use std::fs;
// use std::str;

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = &args[1];
    let contents = fs::read_to_string(filename).expect("Error reading the file");
    let (left, right) = parse_input(&contents);

    let mut similarity: i32 = 0;
    for i in 0..left.len() {
        let count = right.iter().filter(|&x| *x == left[i]).count();
        similarity += count as i32 * left[i];
    }

    println!("Similarity: {}", similarity);
}

fn parse_input(input: &str) -> (Vec<i32>, Vec<i32>) {
    let mut left_numbers: Vec<i32> = Vec::new();
    let mut right_numbers: Vec<i32> = Vec::new();

    let lines = input.lines();
    for line in lines {
        let numbers: Vec<&str> = line.split_whitespace().collect();
        left_numbers.push(numbers[0].parse().unwrap());
        right_numbers.push(numbers[1].parse().unwrap());
    }

    return (left_numbers, right_numbers);
}
