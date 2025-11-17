#!/usr/bin/env python3

from dataclasses import dataclass
import json
import sys
from pathlib import Path

SECTION_DELIMITER = "\n---\n"

def get_full_file_contents(file_path: Path) -> str:
  with open(file_path, 'r', encoding='utf-8') as f:
    return f.read()

@dataclass
class Metadata:
  title: str
  metadata_string: str

@dataclass
class Section:
  markdown_contents: str
  designator: str | None

def return_designator(first_line: str) -> str | None:
  match first_line:
    case "**User**":    return "user"
    case "**Cursor**":  return "agent_response"
    case _:             return None

def process_single_section(raw_section: str) -> Section:
  lines: list[str] = raw_section.strip().split("\n")
  designator: str | None = return_designator(lines[0])

  if designator is not None:
    lines = lines[1:]

  return Section(
    markdown_contents="\n".join(lines).strip(),
    designator=designator
  )

def process_metadata_section(section: str) -> Metadata:
  lines: list[str] = section.strip().split("\n")
  return Metadata(
    title=lines[0].removeprefix("# "),
    metadata_string=lines[1]
  )


def next_section_beginning(given_from_index: int, section_list: list[Section]) -> int:
  actual_start: int = given_from_index + 1

  for index, section in enumerate(section_list[actual_start:], start=actual_start):
    if section.designator is not None:
      return index
  
  return -1

def combine_sections(sections: list[Section]) -> Section:
  assert len(sections) > 0, "Number of sections passed into `combine_sections` should always be greater than 0"
  return Section(
    designator=sections[0].designator,
    markdown_contents=SECTION_DELIMITER.join([s.markdown_contents for s in sections])
  )

def slice_or_end(sections: list[Section], start: int, end: int) -> list[Section]:
  if end == -1:
    return sections[start:]
  return sections[start:end]

def get_sections(full_contents: str) -> tuple[Metadata, list[Section]]:
    [first, *rest] = full_contents.split(SECTION_DELIMITER)
    disjointed_sections = [process_single_section(section) for section in rest]
    corrected_sections: list[Section] = []
    
    i: int = 0
    while i != -1:
      next_index: int = next_section_beginning(i, disjointed_sections)
      corrected_sections.append(combine_sections(slice_or_end(disjointed_sections, i, next_index)))
      i = next_index

    return process_metadata_section(first), corrected_sections


def convert_chat_to_json(input_file_path: str):
    input_path = Path(input_file_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_file_path}")
    
    metadata, section_list = get_sections(get_full_file_contents(input_path))
    output_path = input_path.with_suffix('.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
          "title": metadata.title,
          "metadata_string": metadata.metadata_string,
          "messages": [{
            "markdown_content": section.markdown_contents,
            "designator": section.designator
          } for section in section_list]
        }, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully converted {input_path.name} to {output_path.name}")
    return output_path


def main():
    if len(sys.argv) != 2:
        print("Usage: python cursor_chat_converter.py <input_markdown_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        convert_chat_to_json(input_file)
    except AssertionError as e:
        print(f"Assertion failed: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()