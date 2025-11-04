import mido

def list_midi_ports():
    """Listing all available MIDI input ports."""
    input_ports = mido.get_input_names()  # Returns a list of available MIDI input name ports
    print("Available MIDI ports:")
    for i, port in enumerate(input_ports):
        print(f"{i}: {port}")
    return input_ports 

def select_midi_port(input_ports):
    """Select a MIDI input port if available."""
    if not input_ports:
        raise RuntimeError("No MIDI input ports found.")
    
    port_index = 0  # Default to the first port
    if len(input_ports) > 1:
        port_index = int(input(f"Select MIDI input port [0-{len(input_ports)-1}]: "))
    return input_ports[port_index]

def handle_midi_messages(callback):
    input_ports = list_midi_ports()
    input_port_name = select_midi_port(input_ports)

    with mido.open_input(input_port_name) as inport:
        print(f"Connected to {input_port_name}")
        print("Listening for MIDI input... Press Ctrl+C to stop.")

        while True:
            for msg in inport.iter_pending():
                if msg.type not in ['clock', 'start', 'continue', 'stop']:
                    if msg.type == "note_on" and msg.velocity == 0:
                        # Create a new note_off message
                        note_off_msg = mido.Message('note_off', note=msg.note, channel=msg.channel, time=msg.time)
                        #print("note_off")
                        callback(note_off_msg)
                    else:
                        callback(msg)

def show_information(msg):
    print(msg)

handle_midi_messages(show_information)
