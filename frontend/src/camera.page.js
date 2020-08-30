import React from 'react';
import { Camera } from 'expo-camera';
import { StyleSheet, View, Text } from 'react-native';
import * as Permissions from 'expo-permissions';

import styles from './styles';
import Toolbar from './toolbar.component';
import Gallery from './gallery.component';

export default class CameraPage extends React.Component {
    camera = null;

    state = {
        captures: [],
        capturing: null,
        hasCameraPermission: null,
        cameraType: Camera.Constants.Type.back,
        flashMode: Camera.Constants.FlashMode.off,
    };

    setFlashMode = (flashMode) => this.setState({ flashMode });
    setCameraType = (cameraType) => this.setState({ cameraType });
    handleCaptureIn = () => this.setState({ capturing: true });

    // handleCaptureOut = () => {
    //     if (this.state.capturing)
    //         this.camera.stopRecording();
    // };

    handleShortCapture = async () => {
        const photoData = await this.camera.takePictureAsync();
        this.setState({ capturing: false, captures: [photoData, ...this.state.captures] });
        // var xhr = new XMLHttpRequest();
        // xhr.open('GET', 'http://localhost:5000/');
        var imageBase64 = photoData.base64.replace(/^data:image\/(png|jpg);base64,/, '');
        console.log(imageBase64);
        // // xhr.setRequestHeader('imageData', imageBase64);
        // xhr.send(imageBase64);
        fetch('http://localhost:5000/', {method: 'POST', body: imageBase64})
		  .then(async response => {
		    return response.text().then(async text => {
				console.log(text);
				var wavData = atob(text);
				const audioContext = new AudioContext();
				const arr = Uint8Array.from(wavData, c => c.charCodeAt(0))
				const audio = await audioContext.decodeAudioData(arr.buffer);
				const source = audioContext.createBufferSource();
				source.buffer = audio;
				source.connect(audioContext.destination);
				source.start(0);
		    })
		  })
    };

    // handleLongCapture = async () => {
    //     const videoData = await this.camera.recordAsync();
    //     this.setState({ capturing: false, captures: [videoData, ...this.state.captures] });
    // };

    async componentDidMount() {
        const camera = await Permissions.askAsync(Permissions.CAMERA);
        const audio = await Permissions.askAsync(Permissions.AUDIO_RECORDING);
        let hasCameraPermission = (camera.status === 'granted' && audio.status === 'granted');

        this.setState({ hasCameraPermission });
    };

    render() {
        const { hasCameraPermission, flashMode, cameraType, capturing, captures } = this.state;
		
        if (hasCameraPermission === null) {
            return <View />;
        } else if (hasCameraPermission === false) {
            return <Text>Access to camera has been denied.</Text>;
		}

        return (
            <React.Fragment>
                <View>
                    <Camera
                        type={cameraType}
                        flashMode={flashMode}
                        style={styles.preview}
                        ref={camera => this.camera = camera}
                    />
                </View>

                {captures.length > 0 && <Gallery captures={captures}/>}

                <Toolbar 
                    capturing={capturing}
                    flashMode={flashMode}
                    cameraType={cameraType}
                    setFlashMode={this.setFlashMode}
                    setCameraType={this.setCameraType}
                    // onCaptureIn={this.handleCaptureIn}
                    // onCaptureOut={this.handleShortCapture}
                    // onLongCapture={this.handleLongCapture}
                    onShortCapture={this.handleShortCapture}
                />
            </React.Fragment>
        );
    };
};