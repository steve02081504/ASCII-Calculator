fn main(){let mut a=String::new();std::io::stdin().read_line(&mut a).unwrap();println!("{}",a.trim().chars().map(|c|c as u16).sum::<u16>())}
