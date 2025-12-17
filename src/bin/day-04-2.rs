use ndarray::{Array2, azip, s};
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

    // Make a boolean 2d array representing the grid
    // elements that hold paper rolls are true.
    let mut grid: Array2<bool> = match parse_grid(&content) {
        Ok(grid) => grid,
        Err(e) => {
            eprintln!("Error parsing grid: {}", e);
            process::exit(1);
        }
    };

    let mut removed: usize = 0;

    loop {
        let neighbours: Array2<u8> = count_neighbours(&grid);

        // Find elements with fewer than 4 neighbours that hold rolls of paper.
        let mut accessible: Array2<bool> = Array2::default(grid.dim());
        azip!((a in &mut accessible, &n in &neighbours, &g in &grid) *a = n < 4 && g);

        // Count accessible
        let n_accessible: usize = accessible.iter().filter(|e| **e).count();

        // If no more, stop
        if n_accessible == 0 {
            break;
        }

        // Update grid so that it includes only elements that are not accessible
        // the rest are removed
        azip!((g in &mut grid, &a in &accessible) *g = *g && !a);
        removed += n_accessible;
    }

    // println!("{:?}", grid.map(|e| if *e { '@' } else { '.' }));
    println!("Removed {}", removed);
}

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;
fn parse_grid(grid_string: &String) -> Result<Array2<bool>> {
    let mut flat_data = Vec::new();

    let mut num_rows = 0;
    let mut num_cols = 0;

    for line in grid_string.lines() {
        if num_rows == 0 {
            num_cols = line.chars().count();
        }
        flat_data.extend(line.chars().map(|c| c == '@'));
        num_rows += 1;
    }

    Ok(Array2::from_shape_vec((num_rows, num_cols), flat_data)?)
}

fn count_neighbours(grid: &Array2<bool>) -> Array2<u8> {
    let mut neighbours = Array2::<u8>::zeros(grid.dim());
    let sl_w = grid.ncols() - 1;
    let sl_h = grid.nrows() - 1;
    let west = grid.slice(s![.., ..sl_w]).map(|&e| e.into());
    let north_west = grid.slice(s![..sl_h, ..sl_w]).map(|&e| e.into());
    let north = grid.slice(s![..sl_h, ..]).map(|&e| e.into());
    let north_east = grid.slice(s![..sl_h, 1..]).map(|&e| e.into());
    let east = grid.slice(s![.., 1..]).map(|&e| e.into());
    let south_east = grid.slice(s![1.., 1..]).map(|&e| e.into());
    let south = grid.slice(s![1.., ..]).map(|&e| e.into());
    let south_west = grid.slice(s![1.., ..sl_w]).map(|&e| e.into());

    let mut right_cols = neighbours.slice_mut(s![.., 1..]);
    right_cols += &west;
    let mut bottom_right = neighbours.slice_mut(s![1.., 1..]);
    bottom_right += &north_west;
    let mut bottom_rows = neighbours.slice_mut(s![1.., ..]);
    bottom_rows += &north;
    let mut bottom_left = neighbours.slice_mut(s![1.., ..sl_w]);
    bottom_left += &north_east;
    let mut left_cols = neighbours.slice_mut(s![.., ..sl_w]);
    left_cols += &east;
    let mut top_left = neighbours.slice_mut(s![..sl_h, ..sl_w]);
    top_left += &south_east;
    let mut top_rows = neighbours.slice_mut(s![..sl_h, ..]);
    top_rows += &south;
    let mut top_right = neighbours.slice_mut(s![..sl_h, 1..]);
    top_right += &south_west;

    neighbours
}
