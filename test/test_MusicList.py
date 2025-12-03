import pytest
from unittest.mock import Mock
from tkinter import filedialog
from MusicList import AudioFilesList
import pandas as pd
from docx import Document
import os
from unittest.mock import call

TEST_LIBRARY_FILE = r"C:\Users\dona_\Documents\Python\Musicoterapia\MT_Testingfake\tst_library.txt"

@pytest.fixture
def audio_manager():
    """Fixture to create a fresh instance of AudioFilesList."""
    mgr = AudioFilesList()

    # Prevent GUI attribute errors during tests
    # 1. Mock the GUI widgets (FIX THE ERROR) ---
    mgr.button_generate_list = Mock()
    mgr.label_music_directory_explorer = Mock()
    mgr.label_file_explorer = Mock()
    return mgr

class TestAudioFilesList:
    def test_select_music_folder(self, mocker, audio_manager):

        manager = audio_manager

        # 1. Define the test directory path and contents you want to simulate
        test_music_folder = r"C:\Users\dona_\Documents\Python\Musicoterapia\MT_Testing"

        # 2. Patch the askdirectory to return the test path
        # Patch 'tkinter.filediaglog.askdirectory' as it's used in MysicList.py
        mock_askdirectory = mocker.patch("MusicList.filedialog.askdirectory", return_value=test_music_folder)

        # 3. Call the function under test
        manager.browseMusicFolder()

        # 4. Assert the result is as expected
        assert manager.audio_directory == test_music_folder

        # 5. Check text label updated
        manager.label_music_directory_explorer.configure.assert_called_once_with(
            text=f"Directory Selected: {test_music_folder}"
        )

        # 6. Check button enabled
        manager.button_generate_list.config.assert_called_once_with(state='normal')

        # 7. Check filedialog called
        mock_askdirectory.assert_called_once_with(
            initialdir="/",
            title="Select a Folder"
        )


    def test_save_library_file_success(self, mocker, audio_manager):

        manager = audio_manager        

        # 1. Patch asksaveasfile to return a fake file path
        mock_dialog = mocker.patch("MusicList.filedialog.asksaveasfilename", return_value=TEST_LIBRARY_FILE)

        # 2. Call function being tested
        manager.saveLibraryFile()

        # 3. Assertions
        mock_dialog.assert_called_once_with(filetypes=[("Text Files", "*.txt"),
                ("Excel Files", "*.xlsx"),
                ("Word Files", "*.docx"),
                ("All Files", "*.*")],
                defaultextension=".txt")
        
        # 4. Check parsed components
        assert manager.library_path_name == TEST_LIBRARY_FILE
        assert manager.library_filename == "tst_library.txt"
        assert manager.library_path == r"C:\Users\dona_\Documents\Python\Musicoterapia\MT_Testingfake"

        # 5. Check label updated
        manager.label_file_explorer.configure.assert_called_once_with(text=f"File Opened: {TEST_LIBRARY_FILE}")


    def test_save_library_file_cancelled(self, mocker, audio_manager):
        mock_dialog = mocker.patch("MusicList.filedialog.asksaveasfilename", return_value = "") # User pressed cancel
                                    
        manager = audio_manager

        # 1. Store initial state
        initial_path = manager.library_path
        initial_name = manager.library_filename
        initial_fullpath =  manager.library_path_name

        # 2. Call function being tested
        manager.saveLibraryFile()

        # 3. Check values remain unchanged
        assert manager.library_path == initial_path
        assert manager.library_filename == initial_name
        assert manager.library_path_name == initial_fullpath

        # 4. Check dialog call
        mock_dialog.assert_called_once_with(filetypes = [
            ("Text Files", "*.txt"),
            ("Excel Files", "*.xlsx"),
            ("Word Files", "*.docx"),
            ("All Files", "*.*")    
        ], 
        defaultextension=".txt"
        )


    def test_create_txt_file(self, tmp_path):
        # 1. Create a temporary file path
        tmp_file = tmp_path / "test_library.txt"

        # 2. Create AudioFilesList instance
        mgr = AudioFilesList()

        # 3. Set required attributes
        mgr.library_path_name = str(tmp_file)
        mgr.songs_title_list = ["Song A", "Song B", "Song C"]

        # 4. Call function being tested
        mgr.create_txt_file()

        # 5. Read result
        file_content = tmp_file.read_text(encoding="utf-8")

        # 6. Expected values
        expected = ("File songs library \n"
                    "1: Song A \n"
                    "2: Song B \n"
                    "3: Song C \n"
                    )
        
        # 7. Assert full match
        assert file_content == expected


    def test_create_excel_file(self, tmp_path):
        # 1. Create a temporary file path
        tmp_file = tmp_path / "test_library.xlsx"

        # 2. Create AudioFilesList instance
        mgr = AudioFilesList()

        # 3. Set required attributes
        mgr.library_path_name = str(tmp_file)
        mgr.songs_title_list = ["Song A", "Song B", "Song C"]

        # 4. Call function being tested
        mgr.create_excel_file()

        # 5. Read result
        df = pd.read_excel(tmp_file, index_col=0)

        # 6. Expected values
        expected_df = pd.DataFrame({
            "File songs library": ["Song A", "Song B", "Song C"]
            }) 
        expected_df.index = [1, 2, 3]
        
        # 7. Assert full match
        pd.testing.assert_frame_equal(df,expected_df) 
        expected_df.index = df.index


    def test_create_word_file(self, tmp_path):
        # 1. Create a temporary file path
        tmp_file = tmp_path / "test_library.docx"

        # 2. Create AudioFilesList instance
        mgr = AudioFilesList()

        # 3. Set required attributes
        mgr.library_path_name = str(tmp_file)
        mgr.songs_title_list = ["Song A", "Song B", "Song C"]

        # 4. Call function being tested
        mgr.create_word_file()

        # 5. Read results
        doc = Document(tmp_file)
        doc_content = []
        for p in doc.paragraphs:
            doc_content.append(p.text)
        #return "\n".join(doc_content)

        # 6. Expected values
        expected_doc = ["File songs library",
        "1: Song A \n",
        "2: Song B \n",
        "3: Song C \n",]

        # 7. Assert full match
        assert doc_content == expected_doc


    def test_create_songs_list(self, mocker, audio_manager):
        self.songs_title_list_generated: bool = False
        
        mgr = audio_manager

        # 1. Define the test directory path and contents you want to simulate
        mgr.audio_directory = r"C:\Users\dona_\Documents\Python\Musicoterapia\MT_Testing"

        # 2. Fake directory contents for os.walk
        fake_walk = [
            (mgr.audio_directory, [], ["song1.mp3", "song2.mp3", "image.jpg"])
            ]

        mocker.patch("MusicList.os.walk", return_value=fake_walk)

        # 3. Mock TinyTag.get() for audio files
        fake_tag1 = Mock()
        fake_tag1.title = "Song A"
        
        fake_tag2 = Mock()
        fake_tag2.title = "Song B"


        def fake_tinytag(path):
            if path.endswith("song1.mp3"):
                return fake_tag1
            elif path.endswith("song2.mp3"):
                return fake_tag2
            else:
                raise Exception("Not an audio file")
            
        mocker.patch("MusicList.TinyTag.get", side_effect=fake_tinytag)

        # 4. Mock open() used for error logs
        mock_open = mocker.patch("MusicList.open", mocker.mock_open())

        # 5. Call function being tested
        mgr.create_songs_list()

        # 6. Assertions
        assert mgr.songs_title_list == ["Song A", "Song B"]
        assert mgr.songs_title_list_generated is True

        # 7. Confirm error log for non-audio files was created
        mock_open.assert_called_once()


        def test_create_song_file(sel):
            songs_title_list == ["Song A", "Song B"]

            
    def test_create_song_file_txt(self, mocker):
        # 1. Create AudioFilesList instance
        mgr = AudioFilesList()

        # 2. Define the test file and extention to simulate
        mgr.library_path_name = "dummy.txt"
        mgr.selected_ext = os.path.splitext(mgr.library_path_name)

        # 3. Define Mock dependent functions
        mock_songs = mocker.patch.object(mgr, "create_songs_list")
        mock_txt = mocker.patch.object(mgr, "create_txt_file")
        mock_excel = mocker.patch.object(mgr, "create_excel_file")
        mock_word = mocker.patch.object(mgr, "create_word_file")

        # 4. Call function being tested
        mgr.create_song_file()

        # 5. Assertions
        mock_songs.assert_called_once()
        mock_txt.assert_called_once()
        mock_excel.assert_not_called()
        mock_word.assert_not_called()

    def test_create_song_file_excel(self, mocker):
        # 1. Create AudioFilesList instance
        mgr = AudioFilesList()

        # 2. Define the test file and extention to simulate
        mgr.library_path_name = "dummy.xlsx"
        mgr.selected_ext = os.path.splitext(mgr.library_path_name)

        # 3. Define Mock dependent functions
        mock_songs = mocker.patch.object(mgr, "create_songs_list")
        mock_txt = mocker.patch.object(mgr, "create_txt_file")
        mock_excel = mocker.patch.object(mgr, "create_excel_file")
        mock_word = mocker.patch.object(mgr, "create_word_file")

        # 4. Call function being tested
        mgr.create_song_file()

        # 5. Assertions
        mock_songs.assert_called_once()
        mock_excel.assert_called_once()
        mock_txt.assert_not_called()
        mock_word.assert_not_called()


    def test_create_song_file_word(self, mocker):
        # 1. Create AudioFilesList instance
        mgr = AudioFilesList()

        # 2. Define the test file and extention to simulate
        mgr.library_path_name = "dummy.docx"
        mgr.selected_ext = os.path.splitext(mgr.library_path_name)

        # 3. Define Mock dependent functions
        mock_songs = mocker.patch.object(mgr, "create_songs_list")
        mock_txt = mocker.patch.object(mgr, "create_txt_file")
        mock_excel = mocker.patch.object(mgr, "create_excel_file")
        mock_word = mocker.patch.object(mgr, "create_word_file")

        # 4. Call function being tested
        mgr.create_song_file()

        # 5. Assertions
        mock_songs.assert_called_once()
        mock_word.assert_called_once()
        mock_txt.assert_not_called()
        mock_excel.assert_not_called()


    def test_create_song_file_unsupported(self, mocker, capsys):
        # 1. Create AudioFilesList instance
        mgr = AudioFilesList()

        # 2. Define the test file and extention to simulate
        mgr.library_path_name = "dummy.xyz"
        mgr.selected_ext = os.path.splitext(mgr.library_path_name)

        # 3. Define Mock dependent functions
        mock_songs = mocker.patch.object(mgr, "create_songs_list")
        mock_txt = mocker.patch.object(mgr, "create_txt_file")
        mock_excel = mocker.patch.object(mgr, "create_excel_file")
        mock_word = mocker.patch.object(mgr, "create_word_file")

        # 4. Call function being tested
        mgr.create_song_file()

        # 5. Assertions
        mock_songs.assert_called_once()
        mock_word.assert_not_called()
        mock_txt.assert_not_called()
        mock_excel.assert_not_called()

        
    # def test_run_creates_widgets(self, mocker):
    #     # 1. Mock Tk and Widgets
    #     mock_tk = mocker.patch("MusicList.Tk")

    #     # 2. Define separated button mocks
    #     mock_button = mocker.patch("MusicList.Button")
    #     button_audio = Mock()
    #     button_file = Mock()
    #     button_generate = Mock()
    #     button_exit = Mock()

    #     mock_button.side_effects = [
    #         button_audio,
    #         button_file, 
    #         button_generate,
    #         button_exit
    #     ]

    #     mock_label = mocker.patch("MusicList.Label")
    #     label_music = Mock()
    #     label_file = Mock()
    #     mock_label.side_efect = [label_music, label_file]

    #     mock_mainloop = mock_tk.return_value.mainloop

    #     # 3. Create AudioFilesList instance
    #     mgr = AudioFilesList()

    #     # 4. Call function being tested
    #     mgr.run()


    #     # 5. Assertions
    #     # Tk called to create window
    #     # Labels created
    #     mock_label.assert_any_call(
    #         mock_tk.return_value,
    #         text="Directory Explorer - Audio",
    #         width=75, height=2, fg="blue"
    #     )

    #     mock_label.assert_any_call(
    #         mock_tk.return_value,
    #         text="File Saving *- Library",
    #         width=75, height=2, fg="blue"
    #     )

    #     # Buttons created
    #     mock_button.assert_any_call(
    #         mock_tk.return_value,
    #         text="Browse audio files directory",
    #         command=mgr.browseMusicFolder
    #     )

    #     mock_button.assert_any_call(
    #         mock_tk.return_value,
    #         text="Provide file name",
    #         command=mgr.saveLibraryFile
    #     )

    #     mock_button.assert_any_call(
    #         mock_tk.return_value, 
    #         text="Generate list of files",
    #         command=mgr.create_song_file,
    #     )

    #     mock_button.assert_any_call(
    #         mock_tk.return_value,
    #         text="Exit",
    #         command=exit
    #     )

    #     # 6. mainloop should be called
    #     mock_mainloop.assert_called_once()


def test_run_creates_widgets(mocker, audio_manager):
    mgr = audio_manager

    # Mock Tkinter classes
    mock_tk = mocker.patch("MusicList.Tk")
    mock_label = mocker.patch("MusicList.Label")
    mock_button = mocker.patch("MusicList.Button")

    mgr.run()

    # Verify "Generate list of files" button is created correctly
    expected_call = call(
        mock_tk.return_value,
        text="Generate list of files",
        command=mgr.create_song_file,
        state="disabled",
    ) 

     # 👇 THIS is the correct way to check the button was created
    assert expected_call in mock_button.call_args_list, \
        f"\nExpected call not found.\nAll calls:\n{mock_button.call_args_list}"