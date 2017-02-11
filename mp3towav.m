% Convert all MP3 files in the data folder to WAV

basedir = 'data';
FS = 44100 / 4;
mp3s = dir(fullfile(basedir, '*.mp3'));
for i = 1:length(mp3s)
    filename = mp3s(i).name;
    [wav, fs] = audioread(fullfile(basedir, filename));
    assert(fs == 44100);
    wav = resample(wav, 1, 4);
    [~, basename, ~] = fileparts(filename);
    audiowrite(fullfile(basedir, strcat(basename, '.wav')), wav, FS);
end