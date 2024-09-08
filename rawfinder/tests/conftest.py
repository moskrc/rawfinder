import pytest


@pytest.fixture
def generate_files(tmpdir):
    def _generate_files(file_data):
        # Create a temporary directory
        temp_dir = tmpdir.mkdir("jpeg_files")

        # Generate files based on the input
        for count, ext in file_data:
            for i in range(count):
                file_name = f"file_{i + 1}.{ext}"
                temp_file = temp_dir.join(file_name)

                with open(temp_file, "w") as f:
                    f.write(f"Dummy content for {file_name}")

        return temp_dir

    yield _generate_files
