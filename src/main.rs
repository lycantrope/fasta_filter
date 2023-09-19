use clap::error::ErrorKind;
use clap::{CommandFactory, Parser};
use clap_stdin::FileOrStdin;
use regex::Regex;
use seq_io::fasta::{Reader, Record};
use std::fs::File;
use std::io;
use std::path::PathBuf;
use std::sync::Arc;

#[derive(Parser, Debug)]
#[command(name = "fasta_filter")]
#[command(version = "0.1.0")]
#[command(author = "Chung-Kuan Chen <b97b01045@gmail.com>")]
#[command(about = "A simple to use, efficient FASTA filter CLI Tool", long_about = None)]
struct Cli {
    /// FASTA input (can PIPE from STDIN)
    #[arg(value_name = "FASTA file")]
    input: FileOrStdin,
    /// terminologies to filter (support regex expression)
    #[arg(value_name = "Search term")]
    terms: Vec<Arc<str>>,

    /// Save filtered results to FASTA file, if provided
    #[arg(short, long,)]
    output: Option<PathBuf>,

    /// characters width per line.
    #[arg(short, long, default_value_t = 80)]
    wrap_width:usize,
}

fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();

    let mut reader = Reader::new(cli.input.as_bytes());
    let mut stdout = io::stdout();
    
    let regex_matcher: Arc<[Regex]> = cli
    .terms
    .into_iter()
    .filter_map(|re| {
            let re = re.trim();
            if re.is_empty(){
                None
            }else{
                Regex::new(re).ok()
            }
        }
    )
    .collect();

    if regex_matcher.is_empty(){
        let mut cmd = Cli::command();
        cmd.error(
            ErrorKind::MissingRequiredArgument,
            "No terminolgy was provided.",
        )
        .exit();
    }    

    let text_wrap_width = cli.wrap_width;
    let mut outfile: Option<File> = cli.output.as_ref().and_then(|f| File::create(f).ok());

    while let Some(record) = reader.next().and_then(Result::ok) {
        if record
            .id()
            .is_ok_and(|id| regex_matcher.iter().any(|re| re.is_match(id)))
        {
            record.write_wrap(&mut stdout, text_wrap_width)?;
            if let Some(out) = outfile.as_mut() {
                record.write_wrap(out, text_wrap_width)?;
            }
            continue;
        }

        if record.desc().is_some_and(|desc| {
            desc.is_ok_and(|desc| regex_matcher.iter().any(|re| re.is_match(desc)))
        }) {
            record.write_wrap(&mut stdout, text_wrap_width)?;
            if let Some(out) = outfile.as_mut() {
                record.write_wrap(out, text_wrap_width)?;
            }
        }
    }

    Ok(())
}
