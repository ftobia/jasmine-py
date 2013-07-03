import mockfs
import pytest
import os
import glob

@pytest.fixture
def fs():
    mfs = mockfs.replace_builtins()

    os.path.lexists = mfs.exists
    glob.iglob = mfs.glob

    mfs.add_entries({
        "jasmine.yml": """
            src_files:
              - src/**/*.js
              - src/player.js
              - vendor/test.js
              - vendor/**/*.{js,coffee}
            """,
        "/spec/javascripts/helpers/spec_helper.js": '',
        "/lib/jams/jam_spec.js": '',
        "/src/player.js": '',
        "/src/mixer/mixer.js": '',
        "/src/tuner/fm/fm_tuner.js": '',
        "/spec/javascripts/player_spec.js": '',
        "/spec/javascripts/mixer/mixer_spec.js": '',
        "/spec/javascripts/tuner/fm/fm_tuner_spec.js": '',
        "/spec/javascripts/tuner/am/AMSpec.js": '',
        "/vendor/test.js": '',
        "/vendor/pants.coffee": '',
        "/vendor_spec/pantsSpec.js": '',
    })

    return mfs


@pytest.fixture
def config(fs):
    from jasmine import Config

    return Config("jasmine.yml")


@pytest.mark.usefixtures("fs")
def test_src_files(config):
    assert sorted(config.src_files()) == [
        '/src/mixer/mixer.js',
        '/src/player.js',
        '/src/tuner/fm/fm_tuner.js',
        '/vendor/pants.coffee',
        '/vendor/test.js',
    ]


@pytest.mark.usefixtures("fs")
def test_stylesheets_default(config):
    assert config.stylesheets() == []


@pytest.mark.usefixtures("fs")
def test_helpers_default(config):
    assert config.helpers() == ['/spec/javascripts/helpers/spec_helper.js']


@pytest.mark.usefixtures("fs")
def test_spec_files_default(config):
    assert sorted(config.spec_files()) == [
        '/spec/javascripts/mixer/mixer_spec.js',
        '/spec/javascripts/player_spec.js',
        '/spec/javascripts/tuner/am/AMSpec.js',
        '/spec/javascripts/tuner/fm/fm_tuner_spec.js',
    ]

@pytest.mark.usefixtures("fs")
def test_src_dir_spec_dir(config):
    config.src_dir = 'src'
    config.spec_dir = 'spec'

    config.yaml['src_files'] = ['**/*.js', 'player.js', 'vendor/test.js', 'vendor/**/*.{js,coffee}']

    assert sorted(config.src_files()) == [
        '/src/mixer/mixer.js',
        '/src/player.js',
        '/src/tuner/fm/fm_tuner.js',
    ]

    assert sorted(config.spec_files()) == [
        "/spec/javascripts/mixer/mixer_spec.js",
        "/spec/javascripts/player_spec.js",
        "/spec/javascripts/tuner/am/AMSpec.js",
        "/spec/javascripts/tuner/fm/fm_tuner_spec.js",
    ]